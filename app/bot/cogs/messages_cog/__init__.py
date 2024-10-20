import discord
from discord.ext import commands

from app.models.channels_dataset import CHANNELS
from app.services.cooldown_service import CooldownService
from app.bot.cat_happiness import CatHappiness
from app.services.logging_service import logger


class MessagesCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.cooldown_message_service = CooldownService(240)
        self.cat = CatHappiness()
        self.emotes = {'happy': '<:gato:1180027630871904276>',
                       'sad': '<:gatodespair:1280387632492449946>'}
        self.allowed_channels = [channel.id for channel in CHANNELS]

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" ready!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.is_ready() and message.channel.id in self.allowed_channels:
            happiness = self.cat.get_happiness_from_message(message)
            if happiness is not None:
                return await self._send_emote(message, happiness)

    async def _send_emote(self, message: discord.Message, keyword: str):
        if self.cooldown_message_service.can_execute('keyword'):
            logger.info(
                f'Cooldown service [messages]: added new instance "{keyword}" from message "{message.content}".')
            emote = self.emotes[keyword]
            await message.channel.send(emote)
            return logger.info(f'Cog "{self.__cog_name__}": sent emote "{emote}" in response to message '
                               f'"{message.content}" on channel "{message.channel.name}".')
        return logger.warn(f'Cooldown service [messages]: still in cooldown - "{keyword}": tried message '
                           f'"{message.content}".')
