import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from app.bot import MessagesCog
from app.services.logging_service import logger


class CommandsCog(commands.Cog):
    def __init__(self, bot: discord.Bot, messages_cog: MessagesCog):
        self.bot = bot
        self.messages_cog = messages_cog

    keyword_group = SlashCommandGroup('keywords', 'gato')

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Cog "{self.__cog_name__}" ready!.')

    @keyword_group.command(name='refresh')
    @commands.is_owner()
    async def refresh_keywords(self, ctx: discord.ApplicationContext):
        self.messages_cog.keywords = await self.messages_cog.kw_controller.get_all_keywords()
        logger.info(f'"{self.__cog_name__}": user "{ctx.author.display_name}" used the command "keyword refresh".')
        return await ctx.respond('<:gato:1180027630871904276>', ephemeral=True)

    @refresh_keywords.error
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        logger.error(f'"{self.__cog_name__}": exception occurred - "{error}" : user "{ctx.author.display_name}".')
        await ctx.respond('<:gatodespair:1280387632492449946>', ephemeral=True)
        if isinstance(error, discord.ext.commands.errors.NotOwner):
            return
        raise error
