import random

import discord
from discord.ext import commands
from typing import Union

from app.bot.cogs.happiness_cog import HappinessCog
from app.controllers.emojis_controller import EmojisController
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
        self.allowed_channels = [channel.id for channel in CHANNELS]

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" ready!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if event_is_valid_to_run(message, self.bot):
            return await self._process_message(message)

    async def _process_message(self, message: discord.Message):
        for word in message.content.split():
            if word.lower() in TRISTE.sets + FELIZ.sets:
                user_name = message.author.display_name
                if self.cooldown_users_service.can_execute(message.author.id):
                    logger.info(f'Cooldown service [users] - user "{user_name}": added new instance.')
                    return await self._react_with_emoji(message)
                return logger.warn(f'Cooldown service [users] - user "{user_name}": '
                                   f'still in cooldown - "{message.author.id}".')

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

    async def _react_with_emoji(self, message: discord.Message):
        if random.randint(1, 3) == 3:  # 1 in 3 chance
            emoji = '<:gato:1180027630871904276>' if self.cat.happiness == 'happy' else '<:gatodespair:1280387632492449946>'
            await message.add_reaction(emoji)
            return logger.info(f'"{self.__cog_name__}": triggered keyword reaction "{emoji}" on '
                               f'"{message.channel.name}" channel on message "{message.content}".')
        logger.warn(f'"{self.__cog_name__}": decided to not react to message "{message.content}" on channel'
                    f' "{message.channel.name}".')
