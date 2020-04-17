import discord
from discord.ext import commands
from discord.utils import find
import asyncio
import sqlite3


client = commands.Bot(command_prefix='!', case_insensitive=True)

@client.event
async def on_ready():
    print("I'm ready")

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    await general.send('Chameless plug: https://github.com/MarcOlivierRodrigue/QuoteLibrairieDiscordBot')


#client.run('TOKEN')