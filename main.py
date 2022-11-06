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

"""
This bot uses some notations for the file 
u = use 
g = gain
c = credit
r = repayment
"""

def grab_stats(dict, year=False):
    # this section will read the csv file, and then show the credit, usage, and gain for the month
    # also calculate the leftover i guess
    debug = False

    from customFunctions import fetchCSV
    df = fetchCSV(dict)

    currentMonth = df.loc[df['month'] == datetime.now().month]

    # this is just so that it has every detail, and is not sorted by month
    if year:
        currentMonth = df

    monthUse = currentMonth.loc[currentMonth['notation'] == 'u']
    monthGain = currentMonth.loc[currentMonth['notation'] == 'g']
    monthCredit = currentMonth.loc[currentMonth['notation'] == 'c']
    monthRepay = currentMonth.loc[currentMonth['notation'] == 'r']
    sumUse = monthUse['value'].sum()
    sumGain = monthGain['value'].sum()
    sumCredit = monthCredit['value'].sum()
    sumRepay = monthRepay['value'].sum()

    # this will only for stuff with usage, i dont care about gains and whatnot
    summation = {}              # will store info for usages and categories
    total_ = 0
    uniqueCats = currentMonth['cat'].unique()
    for i in uniqueCats:
        # dictionary to store all values
        # list of values of category
        listCat = currentMonth.loc[(currentMonth['notation'] == 'u') | (currentMonth['notation'] == 'c')]
        listCat = listCat.loc[(listCat['cat'] == str(i))]
        # check if list is empty or not
        if listCat.empty:
            continue
        # find summation of values of category
        listSum = listCat['value'].sum()
        # add it into dictionary
        summation[str(i)] = listSum

    if debug:
        print(sumUse)
        print(sumGain)
        print(sumCredit)
        print(df)
        print(df['month'])

    # do some calculation here to determine what i am using my money for for each month
    # get all categories, and then add up values for each categories

    toSend = "This months use is: " + str(sumUse)
    # loop through the summation dictionary and format stuff out to print
    for key, value in summation.items():
        percentage_ = round((value/sumUse) * 100, 2)
        toSend += "\n   " + str(key) + ": \n         " + str(value) + " (" + str(percentage_) + "%)"
    toSend += "\nThis months gain is: " + str(sumGain)
    toSend += "\nThis months credit use is: " + str(sumCredit)
    toSend += "\nThis months repayment done is: " + str(sumRepay)

    return toSend

# to be moved to the custom functin section to make this read cleaner
def to_send_gen(useAmount, useType, useDesc, amountType, ctx):
    toSend = "Amount " + str(amountType) + ": RM" + str(useAmount) + " \nType: " + str(useType) + " \nDesc: " + str(useDesc)
    toSend += "\nTime logged: " + str(datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))
    toSend += "\nUser is: " + str(ctx.message.author.mention)
    toSend += "\nPlease confirm by using the emoji below ⏬"
    return toSend

def dict_gen(useAmount, useType, useDesc, suffix, ctx):
    # this function generates the dictionary that will be converted into a string to be saved into the file
    dict_ = {
        'cost': useAmount,
        'type': useType,
        'desc': useDesc,
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'hour': datetime.now().hour,
        'minute': datetime.now().minute,
        'user': str(ctx.message.author.mention),
        'suffix': suffix
    }
    return dict_

async def check_valid_value(useAmount, ctx):
    # this function checks for whether the value entered is correct or not, if correct, returns true, else false
    if str(useAmount) == str(0):
        # just to catch some errors
        await ctx.send('Invalid amount, yeet')
        print('debug for valid, false')
        return False
    print('debug for valid, true')
    return True

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

    # note to self that async functions must be awaited if not things go doo doo
    if not await check_valid_value(useAmount, ctx):
        return

    # generates the dict with all the information to be saved
    # multiplies with negative 1 due to usage
    dict = dict_gen(useAmount*-1, useType, useDesc, 'u', ctx)

    # generates and sends the toSend message
    toSend = to_send_gen(useAmount, useType, useDesc, "used", ctx)
    message = await ctx.send(toSend)

    # adds the reaction list
    reactionList = ['✅', '❎']
    for i in reactionList:
        await message.add_reaction(i)

    # this is to check for the correct reaction to the message, must be here for some reason
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
    # uses function to parse out amount, type, desc, and sends it back
    from customFunctions import parseAmount
    useAmount, useType, useDesc = parseAmount(ctx.message.content)

    # note to self that async functions must be awaited if not things go doo doo
    if not await check_valid_value(useAmount, ctx):
        return

    # generates the dict with all the information to be saved
    dict = dict_gen(useAmount, useType, useDesc, 'g', ctx)

    # generates and sends the toSend message
    toSend = to_send_gen(useAmount, useType, useDesc, "gained", ctx)
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

    # note to self that async functions must be awaited if not things go doo doo
    if not await check_valid_value(useAmount, ctx):
        return

    # negative due to credit usage
    # generates the dict with all the information to be saved
    dict = dict_gen(useAmount*-1, useType, useDesc, 'c', ctx)

    # generates and sends the toSend message
    toSend = to_send_gen(useAmount, useType, useDesc, "credited", ctx)
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

@bot.command(brief='Use when money is repayed to dredit. amount, type, desc')
async def repay(ctx, arg):
    # this section IS LITERALLY THE SAME AS THE LAST SECTION, JUST no negative
    # uses function to parse out amount, type, desc, and sends it back
    from customFunctions import parseAmount
    useAmount, useType, useDesc = parseAmount(ctx.message.content)

    # note to self that async functions must be awaited if not things go doo doo
    if not await check_valid_value(useAmount, ctx):
        return

    # negative due to credit usage
    # generates the dict with all the information to be saved
    dict = dict_gen(useAmount, useType, useDesc, 'r', ctx)

    # generates and sends the toSend message
    toSend = to_send_gen(useAmount, useType, useDesc, "credit repayed", ctx)
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

@bot.command(brief='Use to check for stats for the current month.')
async def current(ctx):
    print('this section is for stats')

    dict = {
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'user': str(ctx.message.author.mention)
    }

    toSend = grab_stats(dict)
    await ctx.send(toSend)

@bot.command(brief='Use to check for stats for specific months. Format: month.year (12.2022)')
async def stats(ctx, arg):
    print('this section is for stats')

    # getting the wanted month and year,

    dict = {
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'user': str(ctx.message.author.mention)
    }

    toSend = grab_stats(dict)
    await ctx.send(toSend)

@bot.command(brief='Use to check for lifetime stats.')
async def all(ctx):
    print('this section is for stats')

    dict = {
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'user': str(ctx.message.author.mention)
    }

    toSend = grab_stats(dict, year=True)
    await ctx.send(toSend)

bot.run(botToken)

