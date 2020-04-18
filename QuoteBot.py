import discord
from discord.ext import commands
from discord.utils import find
import asyncio
import sqlite3
import datetime


client = commands.Bot(command_prefix='!quote', case_insensitive=True)

@client.event
async def on_ready():
    print("Quotebot ready!")

@client.event
async def on_guild_join(server):
    for channel in server.text_channels:
        if channel.permissions_for(server.me).send_messages:
            embed = discord.Embed(title="Github", colour=0xecb656, url="https://github.com/MarcOlivierRodrigue/QuoteLibrairieDiscordBot", description="The goal of this discord bot is to allow user of server to manualy register quotes as value and the user as Key. So that they can display later as reminders or funny goofs. You can add it to your server with this [link](https://discordapp.com)")
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_author(name="By Marc-Olivier Rodrigue", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="You can do whatever you want with the source code", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(content="Hi, I'm **Quotebot**! Here to store any ~~goofs or~~ important informations going on here at your leasure. 😎\n\n -  **Get a reminder:** `!quote ?`\n\n -  **Add a new quote:** `!quote title-quote-author` \n\n -  **Display a quote:** `!quote title`\n\n -  **Display a random quote:** `!quote rand`\n\n  -  **Delete a quote:** `!quote delete-title`\n\n **Note:** `title`, `content` and `author` are defined by you when adding a new quote.", embed=embed)

#client.run('TOKEN')