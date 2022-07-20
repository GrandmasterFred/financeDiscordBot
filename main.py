# getting the bot token from the environment
import os
from dotenv import load_dotenv
import logging
import asyncio
import discord
from discord.ext.commands import Bot
from datetime import datetime

# loading environment data
load_dotenv()
botToken = os.getenv('BOT_TOKEN')

# logging in the console
logging.basicConfig(level=logging.INFO)

# start of the bot itself
# this is to turn on messages for reactions i think
intents = discord.Intents.default()
intents.messages = True

# setting the usage key
startWith = "."
bot = Bot(command_prefix=startWith, intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Fred's wallet"))

@bot.event
async def on_message(message):
    # to make sure no infinite loop occours
    if message.author == bot.user:
        return

    if message.content.startswith("magic"):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

# this is the command section of the bot
@bot.command(brief='This makes the bot reply to whatever')
async def r(ctx, arg):
    from customFunctions import removeCommand
    print(removeCommand(ctx.message.content))
    print(ctx.message.content)
    await ctx.send(removeCommand(ctx.message.content))

@bot.command(brief='Use when money is used. amount, type, desc')
async def use(ctx, arg):
    # this section does the part where i use money.
    # uses function to parse out amount, type, desc, and sends it back
    from customFunctions import parseAmount
    useAmount, useType, useDesc = parseAmount(ctx.message.content)
    toSend = "Amount used: RM" + str(useAmount) + " \nType: " + str(useType) + " \nDesc: " + str(useDesc)
    now = datetime.now()
    toSend += "\nTime logged: " + str(now.strftime("%d-%m-%Y_%H:%M:%S"))
    toSend += "\nUser is: " + str(ctx.message.author.mention)
    toSend += "\nPlease confirm by using the emoji below ⏬"
    message = await ctx.send(toSend)
    reactionList = ['✅', '❎']
    for i in reactionList:
        await message.add_reaction(i)

    # this is to check for the correct reaction to the message
    def check(reaction, user):
        print(str(reaction) + str(user) + "conditional: " + str(user == ctx.message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')))
        # checks for the author of the initial message, with the author of the reaction emoji
        return user == ctx.message.author and str(reaction.emoji) in reactionList

    # this is to listen to the correct reaction from the own user
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('No input received, canceling ')
    else:
        print('finished waiting for reaction')
        # this section checks for the reactions and see if its correct or not, and then saves it accordingly
        if str(reaction) == '❎':
            toSend = "Noted, canceling"
            await ctx.send(toSend)
        elif str(reaction) == '✅':
            toSend = "Noted, saving"
            await ctx.send(toSend)


@bot.command(brief='Use when money is used. amount, type, desc')
async def gain(ctx, arg):
    # this section doers the part where i gain money
    print('section to log money gain')

bot.run(botToken)

