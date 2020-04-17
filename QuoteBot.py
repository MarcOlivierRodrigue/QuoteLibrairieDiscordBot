import discord
from discord.ext import commands
import asyncio
import sqlite3


bot = commands.Bot(command_prefix='!', case_insensitive=True)

async def on_ready():
    return await bot.change_presence(activity=discord.Activity(type=1, name='Chameless Plug', url='https://github.com/MarcOlivierRodrigue/QuoteLibrairieDiscordBot'))


#bot.run(TOKEN)