import discord


def event_is_valid_to_run(message: discord.Message, bot: discord.Bot) -> bool:
    return bot.is_ready() and message.author != bot.user
