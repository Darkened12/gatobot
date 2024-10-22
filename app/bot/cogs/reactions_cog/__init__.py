import random

import discord
from discord.ext import commands
from typing import Union, List

from app.bot.cogs.happiness_cog import HappinessCog
from app.controllers.emojis_controller import EmojisController
from app.controllers.keywords_controller import KeywordsController
from app.ext import event_is_valid_to_run
from app.models.channels_dataset import CHANNELS
from app.models.emotional_keywords_dataset import FELIZ, TRISTE
from app.services.logging_service import logger
from app.services.cooldown_service import CooldownService


class ReactionsCog(discord.Cog):
    def __init__(self, bot: discord.Bot, cat_happiness_cog: HappinessCog, emojis_controller: EmojisController):
        self.bot = bot
        self.cat = cat_happiness_cog.cat
        self.emojis_controller = emojis_controller
        self.cooldown_users_service = CooldownService(15)
        self.cooldown_reactions_service = CooldownService(15)
        self.allowed_channels = [channel.id for channel in CHANNELS]
        self.EMOJIS = (1280387632492449946, 1180027630871904276)
        self.KEYWORDS: List[str] = TRISTE.sets + FELIZ.sets

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" ready!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if event_is_valid_to_run(message, self.bot) and message.channel.id in self.allowed_channels:
            return await self._process_message(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        if self._is_valid_reaction(reaction):
            if not self.cooldown_reactions_service.can_execute(reaction.emoji):
                return logger.warn(f'"{self.__cog_name__}" - Cooldown service [reactions] - reaction '
                                   f'"{reaction.emoji}" still in cooldown.')

            logger.info(f'"{self.__cog_name__}" - Cooldown service [reactions] - added new instance: '
                        f'"{reaction.emoji}".')
            await reaction.message.add_reaction(reaction.emoji)
            return logger.info(f'"{self.__cog_name__}" - user "{user.display_name}": added reaction '
                               f'"{reaction.emoji}" on "{reaction.message.channel.name}" channel'
                               f' on message "{reaction.message.content}".')

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        if self._is_valid_reaction(reaction):
            if len(reaction.message.reactions) == 1 and not self._is_valid_message(reaction.message):
                await reaction.message.remove_reaction(reaction.emoji, self.bot.user)
                return logger.info(f'"{self.__cog_name__}": removed reaction "{reaction.emoji}"'
                                   f' on "{reaction.message.channel.name}" channel'
                                   f' on message "{reaction.message.content}" because of user'
                                   f' "{user.display_name}".')

    def _is_valid_message(self, message: discord.Message) -> bool:
        return any(word.lower() in self.KEYWORDS for word in message.content.split())

    def _is_valid_reaction(self, reaction: discord.Reaction) -> bool:
        if reaction.message.channel.id in self.allowed_channels and not reaction.burst:
            try:
                return reaction.emoji.id in self.EMOJIS
            except AttributeError:
                return False
        return False

    async def _process_message(self, message: discord.Message):
        if self._is_valid_message(message):
            user_name = message.author.display_name
            if self.cooldown_users_service.can_execute(message.author.id):
                logger.info(f'Cooldown service [users] - user "{user_name}": added new instance.')
                return await self._react_with_emoji(message)
            return logger.warn(f'Cooldown service [users] - user "{user_name}": '
                               f'still in cooldown - "{message.author.id}".')

    async def _react_with_emoji(self, message: discord.Message):
        if random.randint(1, 3) == 3:  # 1 in 3 chance
            emoji = '<:gato:1180027630871904276>' if self.cat.happiness == 'happy' else '<:gatodespair:1280387632492449946>'
            await message.add_reaction(emoji)
            return logger.info(f'"{self.__cog_name__}": triggered keyword reaction "{emoji}" on '
                               f'"{message.channel.name}" channel on message "{message.content}".')
        logger.warn(f'"{self.__cog_name__}": decided to not react to message "{message.content}" on channel'
                    f' "{message.channel.name}".')
