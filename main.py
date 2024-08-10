import discord
from discord.ext import commands
from discord.utils import get
import time
from database.db import database, uwuImg
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
        if ctx.channel.id not in mainBotChannels:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
            return

        vcData = database.privateVcs.find_one({"owner_id": ctx.author.id})
        if vcData is None:
            await ctx.send("You dont have a private vc")
            return
        members = ""
        for user in vcData["people"]:
            try:
                member = client.get_user(user)
                members += member.name
                members += '\n'
            except Exception as e:
                pass
        embed = discord.Embed(title=f"{ctx.author.name}'s private VC",
                              colour=discord.Colour.dark_teal(),
                              description=members)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)


@client.command(name="removeUser")
async def removeUser(ctx, arg):
    try:
        if ctx.channel.id not in mainBotChannels:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            server = client.get_guild(819441557664169994)
            userId = ctx.author.id
            vcData = database.privateVcs.find_one({"owner_id": userId})
            if vcData is not None:

                member = get(server.members, name=str(arg))

                if member is None:
                    await ctx.send("User does not exists")
                elif member.name == ctx.author.name:
                    await ctx.send("You cannot remove yourself from the vc")
                elif vcData["people"] is None or (member.id not in vcData["people"]):
                    await ctx.send("User already doesnt have access to your vc")
                else:
                    role = get(server.roles, name=vcData["role_id"])
                    await member.remove_roles(role)
                    newPeopleList = vcData["people"].remove(member.id)
                    database.privateVcs.find_one_and_update({"owner_id": userId},
                                                            {"$set": {"people": newPeopleList,
                                                                      "people_num": vcData["people_num"] - 1}})

                    await ctx.send("User removed")
            else:
                await ctx.channel.send("You do not own a private vc!")
    except Exception as e:
        print(e)


@client.command(name="addPoints")
async def addPoints(ctx, arg=None):
    try:
        if ctx.channel.id not in mainBotChannels:
            return
        if ctx.author.id != MY_ID:
            await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
            return
        arg = str(arg).split(",")
        server = client.get_guild(SERVER_ID)
        user = get(server.members, name=arg[0])
        if user is not None:
            userData = database.getUserData(user.id, user.name)
            database.discordData.find_one_and_update({"discord_id": user.id},
                                                     {"$set": {"wallet": userData["wallet"] + int(arg[1])}})
        await ctx.send("Points added")
    except Exception as e:
        print(e)


@client.command(name="fiverrProgress")
async def getFiverrProgress(ctx):
    try:
        if ctx.channel.id not in [1167100338914988112]:
            return
        if ctx.author.id != MY_ID:
            return
        fiverrData = database.fiverrDb.find_one({"isDone": False})
        data = ""
        data += f'sessionCode:{fiverrData["sessionCode"]}' + '\n'
        data += f'progress:{"Not Complete"}' + '\n'
        for i in fiverrData["urls"].keys():
            data += f"    Id:{i}" + '\n'
            data += f"    Url:{fiverrData['urls'][i]['url']}" + '\n'
            data += f"    Progress:{fiverrData['urls'][i]['stage']}" + '\n'
            data += f"    Pages Downloaded:{fiverrData['urls'][i]['stage']}" + '\n'
            data += "\n"
        await ctx.channel.send(data)
    except Exception as e:
        print(e)


@client.command("verify")
async def verifyAccount(ctx, arg=None):
    try:
        if ctx.channel.id not in mainBotChannels:
            pass
    except Exception as e:
        print(e)


client.run(token=settings.botKey)
