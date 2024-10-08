import os
from app.bot import bot
from dotenv import load_dotenv

load_dotenv()
bot.run(os.environ.get('GATO_BOT'))
