import discord
from discord.ext import commands
import asyncio
import sqlite3


bot = commands.Bot(command_prefix='!', case_insensitive=True)

async def on_ready():
    print('Im ready!')


#bot.run(TOKEN)