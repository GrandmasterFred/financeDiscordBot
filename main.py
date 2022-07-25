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

    if str(useAmount) == str(0):
        # just to catch some errors
        await ctx.send('Invalid amount, yeet')
        return


    now = datetime.now()
    dict = {
        'cost': useAmount*-1,
        'type': useType,
        'desc': useDesc,
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'hour': datetime.now().hour,
        'minute': datetime.now().minute,
        'user': str(ctx.message.author.mention),
        'suffix': 'u'
    }
    toSend = "Amount used: RM" + str(useAmount) + " \nType: " + str(useType) + " \nDesc: " + str(useDesc)
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
            message = await ctx.send(toSend)
            from customFunctions import saveToFile
            if saveToFile(dict):
                # this will edit the message that just just sent and add a check mark to double confirm
                await message.edit(content='Noted, saving completed ✅')


@bot.command(brief='Use when money is used. amount, type, desc')
async def gain(ctx, arg):
    # this section IS LITERALLY THE SAME AS THE LAST SECTION, JUST no negative
    # uses function to parse out amount, type, desc, and sends it back
    from customFunctions import parseAmount
    useAmount, useType, useDesc = parseAmount(ctx.message.content)

    if str(useAmount) == str(0):
        # just to catch some errors
        await ctx.send('Invalid amount, yeet')
        return

    now = datetime.now()
    dict = {
        'cost': useAmount,
        'type': useType,
        'desc': useDesc,
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'hour': datetime.now().hour,
        'minute': datetime.now().minute,
        'user': str(ctx.message.author.mention),
        'suffix': 'g'
    }
    toSend = "Amount gained: RM" + str(useAmount) + " \nType: " + str(useType) + " \nDesc: " + str(useDesc)
    toSend += "\nTime logged: " + str(now.strftime("%d-%m-%Y_%H:%M:%S"))
    toSend += "\nUser is: " + str(ctx.message.author.mention)
    toSend += "\nPlease confirm by using the emoji below ⏬"
    message = await ctx.send(toSend)
    reactionList = ['✅', '❎']
    for i in reactionList:
        await message.add_reaction(i)

    # this is to check for the correct reaction to the message
    def check(reaction, user):
        print(str(reaction) + str(user) + "conditional: " + str(
            user == ctx.message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')))
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
            message = await ctx.send(toSend)
            from customFunctions import saveToFile
            if saveToFile(dict):
                # this will edit the message that just just sent and add a check mark to double confirm
                await message.edit(content='Noted, saving completed ✅')

@bot.command(brief='Use when money is credited. amount, type, desc')
async def credit(ctx, arg):
    # this section IS LITERALLY THE SAME AS THE LAST SECTION, JUST no negative
    # uses function to parse out amount, type, desc, and sends it back
    from customFunctions import parseAmount
    useAmount, useType, useDesc = parseAmount(ctx.message.content)

    if str(useAmount) == str(0):
        # just to catch some errors
        await ctx.send('Invalid amount, yeet')
        return

    now = datetime.now()
    dict = {
        'cost': useAmount,
        'type': useType,
        'desc': useDesc,
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'hour': datetime.now().hour,
        'minute': datetime.now().minute,
        'user': str(ctx.message.author.mention),
        'suffix': 'c'
    }
    toSend = "Amount credited: RM" + str(useAmount) + " \nType: " + str(useType) + " \nDesc: " + str(useDesc)
    toSend += "\nTime logged: " + str(now.strftime("%d-%m-%Y_%H:%M:%S"))
    toSend += "\nUser is: " + str(ctx.message.author.mention)
    toSend += "\nPlease confirm by using the emoji below ⏬"
    message = await ctx.send(toSend)
    reactionList = ['✅', '❎']
    for i in reactionList:
        await message.add_reaction(i)

    # this is to check for the correct reaction to the message
    def check(reaction, user):
        print(str(reaction) + str(user) + "conditional: " + str(
            user == ctx.message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')))
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
            message = await ctx.send(toSend)
            from customFunctions import saveToFile
            if saveToFile(dict):
                # this will edit the message that just just sent and add a check mark to double confirm
                await message.edit(content='Noted, saving completed ✅')

@bot.command(brief='Use to check for stats.')
async def stats(ctx, arg):
    print('this section is for stats')

    dict = {
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'user': str(ctx.message.author.mention)
    }
    # this section will read the csv file, and then show the credit, usage, and gain for the month
    # also calculate the leftover i guess
    from customFunctions import fetchCSV
    df = fetchCSV(dict)

    print(df)

    print(df['month'])
    currentMonth = df.loc[df['month'] == datetime.now().month]

    monthUse = currentMonth.loc[currentMonth['notation'] == 'u']
    monthGain = currentMonth.loc[currentMonth['notation'] == 'g']
    monthCredit = currentMonth.loc[currentMonth['notation'] == 'c']
    sumUse = monthUse['value'].sum()
    sumGain = monthGain['value'].sum()
    sumCredit = monthCredit['value'].sum()
    print(sumUse)
    print(sumGain)
    print(sumCredit)

    toSend = "This months use is: " + str(sumUse)
    toSend += "\nThis months gain is: " + str(sumGain)
    toSend += "\nThis months credit use is: " + str(sumCredit)

    await ctx.send(toSend)



bot.run(botToken)

