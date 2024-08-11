import discord
from discord.ext import commands
from database.db import uwuImg
from controller import commandsController, timeController
from models.config import settings, configuration, currentConfiguration

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="rdln.", intents=intents, help_command=None)

currentConfiguration.client = client


@client.event
async def on_ready():
    try:
        x = await client.tree.sync()
        print(f'{x} commands synced')
    except Exception as e:
        print(e)


# @client.command(name="birthday")
# async def birthday(ctx):
#     await ctx.send("9th september. oh how i missed that day. that day was the day my life was complete. before this i was in the computers buffer. after this day i was loaded into the computers main memory which allowed me to order food from foodpanda")
@client.command(name="UwU")
async def UwU(ctx):
    if ctx.channel.id not in configuration.mainBotChannels:
        return
    await ctx.send(uwuImg)


@client.command(name="selfDestruct")
async def selfDestruct(ctx):
    try:
        await commandsController.selfDestruct(ctx)
    except Exception as e:
        print(e)

@client.command(name="shop")
async def shop(ctx):
    try:
        await commandsController.shop(ctx)
    except Exception as e:
        print(e)


@client.command(name="help")
async def help(ctx):
    try:
        await commandsController.help(ctx)
    except Exception as e:
        print(e)


@client.command(name="vcLeaderboard")
async def learderBoard(ctx):
    try:
        await commandsController.vcLeaderboard(ctx)
    except Exception as e:
        print(e)


@client.command(name="stats")
async def my_stats(ctx):
    try:
        await commandsController.stats(ctx)

    except Exception as e:
        print(e)


@client.event
async def on_voice_state_update(member, before, after):
    try:
        await timeController.voiceChannelEvent(member, before, after)
    except Exception as e:
        print(e)


@client.command(name="wallet")
async def wallet(ctx):
    try:
        await commandsController.wallet(ctx)
    except Exception as e:
        print(e)


# @client.command(name="codeStatus")
# async def verifyCode(ctx, arg=None):
#     try:
#         await commandsController.verifyCode(ctx, arg)
#     except Exception as e:
#         print(e)


# @client.command(name="useCode")
# async def useCode(ctx, arg=None):
#     try:
#         await commandsController.useCode(ctx, arg)
#     except Exception as e:
#         print(e)


@client.command(name="setShopStatus")
async def setStatus(ctx, arg=None):
    try:
        await commandsController.setShopStatus(ctx, arg)
    except Exception as e:
        print(e)


@client.command(name="addUser")
async def addUser(ctx, arg=None):
    try:
        await commandsController.addUser(ctx, arg)
    except Exception as e:
        print(e)


@client.command(name="vcUsers")
async def vcUserList(ctx):
    try:
        await commandsController.vcUsersList(ctx)
    except Exception as e:
        print(e)


@client.command(name="removeUser")
async def removeUser(ctx, arg):
    try:
        await commandsController.removeUser(ctx, arg)
    except Exception as e:
        print(e)


@client.command(name="addPoints")
async def addPoints(ctx, arg=None):
    try:
        await commandsController.addPoints(ctx, arg)
    except Exception as e:
        print(e)


# @client.command(name="fiverrProgress")
# async def getFiverrProgress(ctx):
#     try:
#         if ctx.channel.id not in [1167100338914988112]:
#             return
#         if ctx.author.id != MY_ID:
#             return
#         fiverrData = database.fiverrDb.find_one({"isDone": False})
#         data = ""
#         data += f'sessionCode:{fiverrData["sessionCode"]}' + '\n'
#         data += f'progress:{"Not Complete"}' + '\n'
#         for i in fiverrData["urls"].keys():
#             data += f"    Id:{i}" + '\n'
#             data += f"    Url:{fiverrData['urls'][i]['url']}" + '\n'
#             data += f"    Progress:{fiverrData['urls'][i]['stage']}" + '\n'
#             data += f"    Pages Downloaded:{fiverrData['urls'][i]['stage']}" + '\n'
#             data += "\n"
#         await ctx.channel.send(data)
#     except Exception as e:
#         print(e)


@client.command("verify")
async def verifyAccount(ctx, arg=None):
    try:
        pass
    except Exception as e:
        print(e)


client.run(token=settings.botKey)
