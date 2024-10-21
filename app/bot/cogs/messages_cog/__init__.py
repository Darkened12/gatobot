import asyncio
import random
from typing import List

import discord
from discord.ext import commands

from app.controllers.emojis_controller import EmojisController
from app.controllers.keywords_controller import KeywordsController
from app.controllers.links_controller import LinksController
from app.ext import event_is_valid_to_run
from app.models.channels_dataset import CHANNELS
from app.services.cooldown_service import CooldownService
from app.bot.cogs.happiness_cog import HappinessCog
from app.services.logging_service import logger


class MessagesCog(discord.Cog):
    def __init__(self, bot: discord.Bot, keywords_controller: KeywordsController,
                 emojis_controller: EmojisController, links_controller: LinksController):
        self.bot = bot
        self.database = keywords_controller.database
        self.kw_controller = keywords_controller
        self.emoji_controller = emojis_controller
        self.links_controller = links_controller
        self.cooldown_users_service = CooldownService(15)
        self.cooldown_message_service = CooldownService(240)
        self.cooldown_links_service = CooldownService(240)

        self.keywords: List[str] = []
        self.emotes = {'happy': '<:gato:1180027630871904276>',
                       'sad': '<:gatodespair:1280387632492449946>'}
        self.allowed_channels = [channel.id for channel in CHANNELS]

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" starting...')
        await self.database.init()
        logger.info(f'Database is ready!')
        self.keywords = await self.kw_controller.get_all_keywords()
        logger.info(f'cog "{self.__cog_name__}" ready!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not event_is_valid_to_run(message, self.bot):
            return

        if message.channel.id in self.allowed_channels:
            if self.bot.user in message.mentions:
                return await self._reply_to_mention(message)

            return await self._process_message(message)

    async def _process_message(self, message: discord.Message):
        for word in message.content.split():
            for keyword in self.keywords:
                if word.lower() == keyword:
                    user_name = message.author.display_name
                    if self.cooldown_users_service.can_execute(keyword):
                        logger.info(f'Cooldown service [users] - user "{user_name}": added new instance "{keyword}".')
                        return await self._action_chooser(message, keyword)
                    return logger.warn(f'Cooldown service [users] - user "{user_name}": '
                                       f'still in cooldown - "{keyword}".')

    async def _action_chooser(self, message: discord.Message, keyword: str):
        is_keyword_in_emojis = await self.emoji_controller.is_keyword_in_model(keyword)
        is_keyword_in_links = await self.links_controller.is_keyword_in_model(keyword)

        if is_keyword_in_links and is_keyword_in_emojis:
            actions = ['action1', 'action2']
            weights = [70, 30]  # 70% for action1, 30% for action2
            chosen_action = random.choices(actions, weights=weights, k=1)[0]

            if chosen_action == 'action1':
                return await self._send_emote(message, keyword)
            if chosen_action == 'action2':
                return await self._reply_with_random_link(message, keyword)
        if is_keyword_in_links:
            return await self._reply_with_random_link(message, keyword)
        if is_keyword_in_emojis:
            return await self._send_emote(message, keyword)

    async def _reply_to_mention(self, message: discord.Message):
        if self.cooldown_users_service.can_execute(message.author.id):
            logger.info(f'Cooldown service [users]: added new instance "{message.author.id}".')
            return await self._action_chooser(message, random.choice(self.keywords))
        return logger.warn(f'Cooldown service [users]: still in cooldown - "{message.author.id}".')

    async def _send_emote(self, message: discord.Message, keyword: str):
        user_name = message.author.display_name
        if self.cooldown_message_service.can_execute('keyword'):
            logger.info(
                f'Cooldown service [messages] - user "{user_name}": '
                f'added new instance "{keyword}" from message "{message.content}".')
            emote = await self.emoji_controller.get_random_emoji_by_keyword(keyword)
            await message.channel.send(emote.emoji_name)
            return logger.info(f'Cog "{self.__cog_name__}" - user "{user_name}": '
                               f'sent emote "{emote.emoji_name}" in response to message '
                               f'"{message.content}" on channel "{message.channel.name}".')
        return logger.warn(f'Cooldown service [messages] - user "{user_name}": still in cooldown - "{keyword}": '
                           f'tried message "{message.content}".')

    async def _reply_with_random_link(self, message: discord.Message, url: str):
        try:
            link = await self.links_controller.get_random_link_by_keyword(url)
        except ValueError:
            return

        user_name = message.author.display_name
        if self.cooldown_links_service.can_execute(url):
            logger.info(
                f'Cooldown service [links] - user "{user_name}": added new instance "{url}" '
                f'from message "{message.content}".')
            async with message.channel.typing():
                await asyncio.sleep(2)
                await message.reply(link.url, mention_author=False)
                return logger.info(f'triggered keyword reaction "{url}" on "{message.channel.name}" channel'
                                   f' on message "{message.content}".')

        logger.warn(f'Cooldown service [links] - user "{user_name}": still in cooldown - "{url}".')
