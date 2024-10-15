import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from datetime import datetime

from app.bot import ReactToMessagesCog
from app.services.logging_service import logger


class CommandsCog(commands.Cog):
    def __init__(self, bot: discord.Bot, react_to_messages_cog: ReactToMessagesCog):
        self.bot = bot
        self.react_to_messages_cog = react_to_messages_cog

    keyword_group = SlashCommandGroup('keywords', 'gato', checks=[commands.is_owner()])

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Cog "{self.__cog_name__}" ready at "{datetime.now()}".')

    @keyword_group.command(name='refresh')
    async def refresh_keywords(self, ctx: discord.ApplicationContext):
        self.react_to_messages_cog.keywords = await self.react_to_messages_cog.kw_controller.get_all_keywords()
        logger.info(f'"{self.__cog_name__}": user "{ctx.author.display_name}" used the command "keyword refresh".')
        return await ctx.respond('<:gato:1180027630871904276>', ephemeral=True)

    @refresh_keywords.error
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        logger.error(f'Exception occurred - "{error}" : user "{ctx.author.display_name}".')
        await ctx.respond('<:gatodespair:1280387632492449946>', ephemeral=True)
        raise error
