import discord
from discord.ext import commands
from app.bot.cat_happiness import CatHappiness
from app.models.channels_dataset import CHANNELS
from app.services.logging_service import logger


class HappinessCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.cat = CatHappiness()

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
            else:
                await self.bot.close()
                raise TypeError(f'channel "{channel_model.id}" is not a TextChannel.')
        logger.info(f'cog "{self.__cog_name__}" ready!')

    async def _evaluate_channel_happiness(self, channel: discord.TextChannel):
        async for message in channel.history(limit=100):
            self.cat.get_happiness_from_message(message)


