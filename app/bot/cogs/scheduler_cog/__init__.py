import asyncio

import discord
from discord.ext import commands

from app.bot import HappinessCog
from app.models.channels_dataset import CHANNELS
from app.services import parallel_task_runner_service
from app.services.logging_service import logger


class SchedulerCog(commands.Cog):
    def __init__(self, bot: discord.Bot, cat_happiness_cog: HappinessCog):
        self.bot = bot
        self.cat = cat_happiness_cog.cat

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" starting...')
        for channel_model in CHANNELS:
            channel = self.bot.get_channel(channel_model.id)
            if isinstance(channel, discord.TextChannel):
                parallel_task_runner_service.run_parallel_task(self._scheduled_cat_sender(
                    channel, channel_model.sleep_time_in_seconds))
            else:
                await self.bot.close()
                raise TypeError(f'channel "{channel_model.id}" is not a TextChannel.')
        logger.info(f'cog "{self.__cog_name__}" ready!')

    async def _scheduled_cat_sender(self, channel: discord.TextChannel, time_in_seconds: int):
        logger.info(f'Started scheduled task: cat_sender will be executed on channel "{channel.name}" '
                    f'in {int(time_in_seconds/60)} minutes.')
        await asyncio.sleep(time_in_seconds)
        await channel.send(self.emotes[self.cat.happiness])
        logger.info(f'Scheduled task: cat_sender executed successfully on channel "{channel.name}". '
                    f'Cat happiness level was "{self.cat.happiness_level}": "{self.cat.happiness}".')