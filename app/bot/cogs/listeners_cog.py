import asyncio
import os
import discord
from discord.ext import commands
from datetime import datetime
from .channels import CHANNELS, ChannelsModel

from app.services.database_service import DatabaseService
from app.services.logging_service import logger
from app.controllers.gifs_controller import GifsController
from app.services import randomizer_cat_service, parallel_task_runner_service


class ListenersCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.gifs_controller = GifsController(database_service=DatabaseService(os.environ.get('DATABASE_SECRET')))

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Cog "{self.__cog_name__}" starting at "{datetime.now()}".')

        await self.gifs_controller.database_service.init()
        logger.info('Database initiated successfully!')

        for channel_model in CHANNELS:
            parallel_task_runner_service.run_parallel_task(self.__cat_sender(channel_model))

        logger.info(f'Cog "{self.__cog_name__}" ready at "{datetime.now()}".')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    async def __cat_sender(self, channel_model: ChannelsModel):
        channel = self.bot.get_channel(channel_model.id)
        time_in_seconds = channel_model.sleep_time_in_seconds
        while True:
            cat = await randomizer_cat_service.get_random_cat(self.gifs_controller)
            await channel.send(cat)
            logger.info(f'gif/emoji sent to "{channel.name}" of id "{channel.id}": "{cat}"')
            await asyncio.sleep(time_in_seconds)
