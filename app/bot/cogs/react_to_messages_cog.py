import random
import discord
import asyncio
from discord.ext import commands
from typing import Union, List
from app.bot.channels import CHANNELS
from app.controllers.emojis_controller import EmojisController
from app.controllers.keywords_controller import KeywordsController
from app.controllers.links_controller import LinksController
from app.services.logging_service import logger
from app.services.cooldown_service import CooldownService


class ReactToMessagesCog(discord.Cog):
    def __init__(self, bot: discord.Bot, keywords_controller: KeywordsController,
                 emoji_controller: EmojisController, links_controller: LinksController):
        self.bot = bot
        self.database = keywords_controller.database
        self.kw_controller = keywords_controller
        self.emoji_controller = emoji_controller
        self.links_controller = links_controller
        self.cooldown_service_reactions = CooldownService(120)
        self.cooldown_service_users = CooldownService(15)
        self.allowed_channels = [channel.id for channel in CHANNELS]
        self.keywords: List[str] = []

    @commands.Cog.listener()
    async def on_ready(self):
        await self.database.init()
        logger.info(f'Database is ready.')
        self.keywords = await self.kw_controller.get_all_keywords()
        logger.info(f'cog "{self.__cog_name__}" ready.')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.is_ready():
            if message.author != self.bot.user and message.channel.id in self.allowed_channels:
                if self.bot.user.mention in message.mentions:
                    return await self._react_to_mention(message)

                return await self._react_to_message(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        if reaction.message.channel.id in self.allowed_channels and not reaction.burst:
            try:
                if reaction.emoji.id in [1280387632492449946, 1180027630871904276]:
                    await reaction.message.add_reaction(reaction.emoji)
                    return logger.info(f'added reaction "{reaction.emoji}" on "{reaction.message.channel.name}" channel'
                                       f' on message "{reaction.message.content}".')
            except AttributeError:
                pass

    async def _react_to_mention(self, message: discord.Message):
        if self.cooldown_service_users.can_execute(message.author.id):
            logger.info(f'Cooldown service [users]: added new instance "{message.author.id}".')
            return await self._action_chooser(message, random.choice(self.keywords))
        return logger.warn(f'Cooldown service [users]: still in cooldown - "{message.author.id}".')

    async def _react_to_message(self, message: discord.Message):
        for word in message.content.split():
            for keyword in self.keywords:
                if word.lower() == keyword:
                    if self.cooldown_service_reactions.can_execute(keyword):
                        logger.info(f'Cooldown service [reactions]: added new instance "{keyword}".')
                        return await self._action_chooser(message, keyword)
                    return logger.warn(f'Cooldown service [reactions]: still in cooldown - "{keyword}".')

    async def _action_chooser(self, message: discord.Message, keyword: str):
        is_keyword_in_emojis = await self.emoji_controller.is_keyword_in_model(keyword)
        is_keyword_in_links = await self.links_controller.is_keyword_in_model(keyword)

        if is_keyword_in_links and is_keyword_in_emojis:
            actions = ['action1', 'action2']
            weights = [70, 30]  # 70% for action1, 30% for action2
            chosen_action = random.choices(actions, weights=weights, k=1)[0]

            if chosen_action == 'action1':
                return await self._reply_with_random_link(message, keyword)
            if chosen_action == 'action2':
                return await self._react_with_random_emoji(message, keyword)
        if is_keyword_in_links:
            return await self._reply_with_random_link(message, keyword)
        if is_keyword_in_emojis:
            return await self._react_with_random_emoji(message, keyword)

    async def _reply_with_random_link(self, message: discord.Message, keyword: str):
        async with message.channel.typing():
            try:
                link = await self.links_controller.get_random_link_by_keyword(keyword)
            except ValueError:
                return
            await asyncio.sleep(1)
            await message.reply(link.url, mention_author=False)
            return logger.info(f'triggered keyword reaction "{keyword}" on "{message.channel.name}" channel'
                               f' on message "{message.content}".')

    async def _react_with_random_emoji(self, message: discord.Message, keyword: str):
        try:
            emoji = await self.emoji_controller.get_random_emoji_by_keyword(keyword)
        except ValueError:
            return

        await message.add_reaction(emoji.emoji_name)
        return logger.info(f'triggered keyword reaction "{keyword}" on "{message.channel.name}" channel'
                           f' on message "{message.content}".')
