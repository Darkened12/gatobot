import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from datetime import datetime

from app.controllers.links_controller import LinksController, AlreadyExistsError
from app.services.logging_service import logger


class CommandsCog(commands.Cog):
    def __init__(self, bot: discord.Bot, gifs_controller: LinksController):
        self.bot = bot
        self.controller = gifs_controller

    gif_group = SlashCommandGroup('gif', 'gato')

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Cog "{self.__cog_name__}" ready at "{datetime.now()}".')

    @gif_group.command(name='add', description='adds a gif to the gato database')
    async def add_gif(self, ctx: discord.ApplicationContext, url: str):
        try:
            await self.controller.add_gif(
                gif=url,
                user=ctx.author
            )
            await ctx.respond(f"Gif {url} added!", ephemeral=True)
            return logger.info(f'user "{ctx.author}" added the gif "{url}".')
        except AlreadyExistsError:
            await ctx.respond(f"Error! Either the gif already exists or something else happened!", ephemeral=True)
            return logger.error(f'error {AlreadyExistsError} ocurred while executing command "add" - user: {ctx.author}'
                                f' gif: {url}')

    @add_gif.error
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        # if isinstance(error, commands.NotOwner):
        #     await ctx.respond("Sorry, only the bot owner can use this command.", ephemeral=True)
        #     logger.warning(f'User "{ctx.author.display_name}" tried to use the command "gif add".')
        # else:
            logger.error(f'Exception occurred - "{error}" : user "{ctx.author.display_name}".')
            await ctx.respond('An unknown error occurred.', ephemeral=True)
            raise error
