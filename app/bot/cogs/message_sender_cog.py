import asyncio
from typing import Optional

import discord
from discord.ext import commands

from app.models.channels_dataset import CHANNELS
from app.models.emotional_keywords_dataset import TRISTE, FELIZ
from app.services import parallel_task_runner_service
from app.services.cooldown_service import CooldownService
from app.bot.cat_happiness import CatHappiness
from app.services.logging_service import logger


class MessageSenderCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.cooldown_message_service = CooldownService(120)
        self.cat = CatHappiness()
        self.emotes = {'happy': '<:gato:1180027630871904276>',
                       'sad': '<:gatodespair:1280387632492449946>'}
        self.allowed_channels = [channel.id for channel in CHANNELS]

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" starting...')

        for channel_model in CHANNELS:
            channel = self.bot.get_channel(channel_model.id)
            if isinstance(channel, discord.TextChannel):
                logger.info(f'"{self.__cog_name__}": evaluating happiness on "{channel.name}" channel')
                await self._evaluate_channel_happiness(channel)
                logger.info(f'"{self.__cog_name__}": evaluation done on "{channel.name}". happiness level '
                            f'{self.cat.happiness_level}. Status: "{self.cat.happiness}"')

                parallel_task_runner_service.run_parallel_task(self._scheduled_cat_sender(
                    channel, channel_model.sleep_time_in_seconds))
            else:
                await self.bot.close()
                raise TypeError(f'channel "{channel_model.id}" is not a TextChannel.')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.is_ready() and message.channel.id in self.allowed_channels:
            happiness = self._get_happiness_from_message(message)
            if happiness is not None:
                return await self._send_emote(message, happiness)

    async def _scheduled_cat_sender(self, channel: discord.TextChannel, time_in_seconds: int):
        logger.info(f'Started scheduled task: cat_sender will be executed on channel "{channel.name}" '
                    f'in {int(time_in_seconds/60)} minutes.')
        await asyncio.sleep(time_in_seconds)
        await channel.send(self.emotes[self.cat.happiness])
        logger.info(f'Scheduled task: cat_sender executed successfully on channel "{channel.name}". '
                    f'Cat happiness level was "{self.cat.happiness_level}": "{self.cat.happiness}".')

    async def _evaluate_channel_happiness(self, channel: discord.TextChannel):
        async for message in channel.history(limit=100):
            self._get_happiness_from_message(message)

    async def _send_emote(self, message: discord.Message, keyword: str):
        if self.cooldown_message_service.can_execute('keyword'):
            return await message.channel.send(self.emotes[keyword])

    def _get_happiness_from_message(self, message: discord.Message) -> Optional[str]:
        for word in message.content.split():
            if word.lower() in FELIZ.sets:
                self.cat.make_happy()
                return 'happy'
            if word.lower() in TRISTE.sets:
                self.cat.make_sad()
                return 'sad'
