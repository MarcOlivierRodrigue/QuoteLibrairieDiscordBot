import discord
from discord.ext import commands
from discord.utils import find
import asyncio
import sqlite3
from sqlite3 import Error
import datetime


client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command('help')

#==============================================
#Definition the help Message
#==============================================
def getHelpText():
    helpMessage = "Hi, I'm **Quotebot**! Here to store any ~~goofs or~~ important informations going on here at your leasure. 😎\n\n -  **Get a reminder:** `!help`\n\n -  **Add a new quote:** `!add \"title\" \"content\" \"author\"` \n\n -  **Display a quote:** `!show \"title\"`\n\n -  **Display a random quote:** `!random`\n\n  -  **Delete a quote:** `!delete \"title\"`\n\n **Note:** `title`, `content` and `author` are defined by you when adding a new quote."
    embed = discord.Embed(title="Github", colour=0xecb656, url="https://github.com/MarcOlivierRodrigue/QuoteLibrairieDiscordBot", description="The goal of this discord bot is to allow user of guild to manualy register quotes as value and the user as Key. So that they can display later as reminders or funny goofs. You can add it to your guild with this [link](https://discordapp.com)")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="By Marc-Olivier Rodrigue", url="https://github.com/MarcOlivierRodrigue/QuoteLibrairieDiscordBot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="You can do whatever you want with the source code", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.timestamp = datetime.datetime.utcnow()
    return [helpMessage , embed]

#==============================================
#When the bot is up and running
#==============================================
def connectSqlite():
    result = True
    try:
        db = sqlite3.connect('quotes.sqlite')
    except Error as e:
        print(e)
        result = False
    return [result, db]

@client.event
async def on_ready():
    db = connectSqlite()
    if db[0]:
        c = db[1].cursor()
        c.execute("CREATE TABLE IF NOT EXISTS quotes(title TEXT, content TEXT, author TEXT, guild_id TEXT, date TEXT, addedBy TEXT)")
        print("Quotebot ready!")
    else: 
        print("ERROR: Unable to connect to the Sqlite database")



#==============================================
#Display the Help message when the bot is added to a server 
#==============================================
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            entryTexts = getHelpText()
            await channel.send(content=entryTexts[0], embed=entryTexts[1])


#==============================================
#General Error Handler
#==============================================
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.InvalidEndOfQuotedStringError):
        await ctx.send("**Error**: Might be one of these issues \n**1.** Make sure each parameter is closed properly with a \". \n**2.** Add a \ before each quotation mark **inside** a single parameter.")


#==============================================
#!add command
#==============================================
@client.command()
async def add(ctx, title: str, content: str, author: str):
    message = "**New quote** {} \n*\"{}\"* \n- {} \n added by {}"
    guild_id = ctx.guild.id
    date = (datetime.datetime.utcnow()).strftime('%Y-%m-%d %H:%M')
    addedBy = ctx.author.name

    db = connectSqlite()
    if db[0]:
        c = db[1].cursor()
        c.execute("SELECT * FROM quotes WHERE guild_id = ? AND title = ?", (guild_id, title))
        result = c.fetchone()
        if result is None:
            c.execute("INSERT INTO quotes VALUES (?, ?, ?, ?, ?, ?)", (title, content, author, guild_id, date, addedBy))
            await ctx.send(message.format(title, content, author, addedBy)) 
        elif result is not None:
            message = "**Updated quote**\n from:\n{} \n*\"{}\"* - {}\nAdded by {}, {}\n\nto:\n{} \n*\"{}\"*  - {}\nUpdated by {}, {}"
            c.execute("UPDATE quotes SET title = ?, content = ?, author = ?, guild_id = ?, date = ?, addedBy = ?  WHERE guild_id = ? AND title = ?", (title, content, author, guild_id, date, addedBy, guild_id, title))
            await ctx.send(message.format(result[0], result[1], result[2], result[5], result[4], title, content, author, addedBy, date))
        db[1].commit()
        c.close()
        db[1].close()
    else:
        await ctx.send("**ERROR**: Unable to connect to the Sqlite database")


@add.error
async def add_missingArg(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Error**: The `title`, `content` and `author` parameters are all mendatory.")

#==============================================         
#!help command
#==============================================
@client.command()
async def help(ctx):
    helpText = getHelpText()
    await ctx.channel.send(content=helpText[0], embed=helpText[1])


#client.run('TOKEN')