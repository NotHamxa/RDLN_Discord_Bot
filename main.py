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
# @client.command("remove")
# async def removeCommand(ctx,arg):
#     roleName = "👑 President"
#     memberName = arg
#     role = discord.utils.get(ctx.guild.roles, name=roleName)
#     member = discord.utils.get(ctx.guild.members, name=memberName)
#
#     await member.remove_roles(role)

@client.event
async def on_ready():
    try:
        x = await client.tree.sync()
        print(f'{len(x)} commands synced')
    except Exception as e:
        print(e)


# @client.command(name="birthday")
# async def birthday(ctx):
#     await ctx.send("9th september. oh how i missed that day. that day was the day my life was complete. before this i was in the computers buffer. after this day i was loaded into the computers main memory which allowed me to order food from foodpanda")

# @client.command(name="UwU")
# async def UwU(interaction:discord.Interaction):
#     if interaction.channel.id not in configuration.mainBotChannels:
#         return
#     await interaction.response.send_message(uwuImg)


@client.tree.command(name="self-destruct")
async def selfDestruct(ctx):
    try:
        await commandsController.selfDestruct(ctx)
    except Exception as e:
        print(e)

@client.tree.command(name="shop")
async def shop(interaction:discord.Interaction):
    try:
        await commandsController.shop(interaction)
    except Exception as e:
        print(e)


@client.tree.command(name="help")
async def help(interaction:discord.Interaction):
    try:
        await commandsController.help(interaction)
    except Exception as e:
        print(e)


@client.tree.command(name="vc-leaderboard")
async def leaderBoard(interaction:discord.Interaction):
    try:
        await commandsController.vcLeaderboard(interaction)
    except Exception as e:
        print(e)


@client.tree.command(name="stats")
async def my_stats(interaction:discord.Interaction):
    try:
        await commandsController.stats(interaction)

    except Exception as e:
        print(e)


@client.event
async def on_voice_state_update(member, before, after):
    try:
        await timeController.voiceChannelEvent(member, before, after)
    except Exception as e:
        print(e)


@client.tree.command(name="wallet")
async def wallet(interaction:discord.Interaction):
    try:
        await commandsController.wallet(interaction)
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


@client.tree.command(name="set-shop-status")
async def setStatus(interaction:discord.Interaction, status:str):
    try:
        await commandsController.setShopStatus(interaction, status)
    except Exception as e:
        print(e)


@client.tree.command(name="add-user")
async def addUser(interaction:discord.Interaction, username:str):
    try:
        await commandsController.addUser(interaction, username)
    except Exception as e:
        print(e)


@client.tree.command(name="vc-users")
async def vcUserList(interaction:discord.Interaction):
    try:
        await commandsController.vcUsersList(interaction)
    except Exception as e:
        print(e)


@client.tree.command(name="remove-user")
async def removeUser(interaction:discord.Interaction, username:str):
    try:
        await commandsController.removeUser(interaction, username)
    except Exception as e:
        print(e)


@client.tree.command(name="verify")
async def verifyAccount(interaction:discord.Interaction,email:str):
    try:
        await commandsController.verifyAccount(interaction,email)
    except Exception as e:
        print(e)

@client.tree.command(name="clear-db")
async def clearDB(interaction:discord.Interaction):
    try:
        await commandsController.clearDB(interaction)
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


@client.tree.command(name="add-points")
async def addPoints(interaction:discord.Interaction, username:str,points:str):
    try:
        await commandsController.addPoints(interaction, username,points)
    except Exception as e:
        print(e)


client.run(token=settings.botKey)
