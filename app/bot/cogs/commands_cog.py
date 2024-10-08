import discord
from discord.ext import commands

from app.controllers.gifs_controller import GifsController, AlreadyExistsError


class CommandsCog(discord.Cog):
    def __int__(self, bot: discord.Bot, gifs_controller: GifsController):
        self.bot = bot
        self.controller = gifs_controller

    @commands.group(name='gif')
    async def gif_group(self, ctx: discord.ApplicationContext):
        return await ctx.respond('Available subcommads: add', ephemeral=True)

    @gif_group.command(name='add', description='adds a gif to the gato database')
    async def add_gif(self, ctx: discord.ApplicationContext, url: str):
        try:
            await self.controller.add_gif(
                gif=url,
                user=ctx.author
            )
            return await ctx.respond(f"Gif {url} added!", ephemeral=True)
        except AlreadyExistsError:
            return await ctx.respond(f"Error! Either the gif already exists or something else happened!")
