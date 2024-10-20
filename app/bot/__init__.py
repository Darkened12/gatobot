import os
import discord
from dotenv import load_dotenv as __load_dotenv

from app.bot.cogs.messages_cog import MessagesCog
from app.bot.cogs.reactions_cog import ReactionsCog
from app.bot.cogs.commands_cog import CommandsCog
from app.bot.cogs.happiness_cog import HappinessCog
from app.bot.cogs.scheduler_cog import SchedulerCog

from app.services.database_service import DatabaseService

from app.controllers.links_controller import LinksController
from app.controllers.keywords_controller import KeywordsController
from app.controllers.emojis_controller import EmojisController


__load_dotenv()
__intents = discord.Intents.default()
__intents.messages = True
__intents.message_content = True
__intents.reactions = True

bot = discord.Bot(intents=__intents, owner_id=int(os.environ.get('OWNER_ID')))
__database = DatabaseService(dsn_connector='sqlite+aiosqlite:///', dsn=os.environ.get('DATABASE'))
__controller = LinksController(__database)

__react_to_messages_cog = ReactionsCog(
    bot=bot,
    keywords_controller=KeywordsController(__database),
    emoji_controller=EmojisController(__database),
    links_controller=LinksController(__database),
)

bot.add_cog(__react_to_messages_cog)
bot.add_cog(CommandsCog(bot, __react_to_messages_cog))
bot.add_cog(MessagesCog(bot))
bot.add_cog(HappinessCog(bot))
bot.add_cog(SchedulerCog(bot))
