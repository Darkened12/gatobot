import os
import discord
from dotenv import load_dotenv as __load_dotenv

from app.services.database_service import DatabaseService
from app.controllers.gifs_controller import GifsController
from app.bot.cogs.listeners_cog import ListenersCog
from app.bot.cogs.commands_cog import CommandsCog


__load_dotenv()
__intents = discord.Intents.default()
__intents.messages = True

bot = discord.Bot(intents=__intents, owner_id=os.environ.get('OWNER_ID'))
__database = DatabaseService(dsn_connector='sqlite+aiosqlite:///', dsn=os.environ.get('DATABASE'))
__controller = GifsController(__database)

bot.add_cog(ListenersCog(bot, __controller))
bot.add_cog(CommandsCog(bot, __controller))

