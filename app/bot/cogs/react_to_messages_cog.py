import discord
from discord.ext import commands
from typing import Union
from app.bot.channels import CHANNELS
from app.services.logging_service import logger

keywords = {
    "meow": "😺",
    "ronronar": "😸",
    "feliz": "😊",
    "triste": "😿",
    "brincar": "🐾",
    "catnip": "😻",
    "dormir": "💤",
    "comida": "🍲",
    "caçar": "🐱‍👓",
    "arranhar": "😼",
    "miado": "😽",
    "miau": "😹",
    "gatinho": "😺",
    "gatona": "😽",
    "gato": "😽",
    "fofo": "😻",
    "ronron": "😸",
    "pet": "🐾",
    "fudeu": '<:gatodespair:1280387632492449946>',
    "perdemo": '<:gatodespair:1280387632492449946>',
    "perdi": '<:gatodespair:1280387632492449946>',
}


class ReactToMessagesCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.allowed_channels = [channel.id for channel in CHANNELS]

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'cog "{self.__cog_name__}" ready.')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author != self.bot.user and message.channel.id in self.allowed_channels:
            for word in message.content.split():
                if word.lower() in keywords.keys():
                    emoji = keywords[word.lower()]
                    await message.add_reaction(emoji)
                    return logger.info(f'triggered keyword reaction "{emoji}" on "{message.channel.name}" channel'
                                       f' on message "{message.content}".')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]):
        if reaction.message.channel.id in self.allowed_channels:
            if reaction.emoji.id in [1280387632492449946, 1180027630871904276]:
                await reaction.message.add_reaction(reaction.emoji)
                return logger.info(f'added reaction "{reaction.emoji}" on "{reaction.message.channel.name}" channel'
                                   f' on message "{reaction.message.content}".')
