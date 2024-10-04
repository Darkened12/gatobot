import os

import discord
import asyncio
import random

from datetime import datetime
from dotenv import load_dotenv
from typing import List

load_dotenv()

intents = discord.Intents.default()
intents.messages = True

bot = discord.Bot(intents=intents)

CHANNELS: List[int] = [974759972036542484]


async def send_random_cat():
    for channel_id in CHANNELS:
        channel = bot.get_channel(channel_id)
        selected_item = random.choices(
            EMOJIS,
            weights=[40, 40, 20, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            k=1
        )[0]
        await channel.send(selected_item)


async def sleep():
    await asyncio.sleep(1800)


@bot.event
async def on_ready():
    print(f'Logged at {datetime.now()} as {bot.user}')

    while True:
        await send_random_cat()
        await sleep()


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        return await message.reply(random.choice(EMOJIS))

    if message.reference:
        original_message = await message.channel.fetch_message(message.reference.message_id)
        if bot.user in original_message.mentions:
            return await message.reply(random.choice(EMOJIS))


bot.run(os.environ.get('GATO_BOT'))
