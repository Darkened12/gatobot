import discord
from discord.ext import commands


class CommandsCog(discord.Cog):
    def __int__(self, bot: discord.Bot):
        self.bot = bot

    @commands.group(name='gif')
    async def gif_group(self, ctx: discord.ApplicationContext):
        return await ctx.respond('Available subcommads: add', ephemeral=True)

    @gif_group.command(name='add', description='adds a gif to the gato database')
    async def add_gif(self, ctx: discord.ApplicationContext, url: str):

        await ctx.send(f"Gif {url} added!")