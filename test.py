import discord
from discord.ext import commands
from discord.utils import get
from db import database

SECRET_KEY = "MTE2NjgxNTMzNzM4NDI2MzgzMA.G20Jyo.lAOSXqeJNgwQRXFC49JEPqgEp5T0F1CWG9-JdA"
BOT_ANNOUNCEMENTS_CHANNEL_ID = 1178684719144128533
PRIVATE_CHANNELS_CATEGORY_ID = 1190401067813453984
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="rdln.", intents=intents, help_command=None)


@client.command(name="test")
async def createVc(ctx):
    userId = ctx.author.id
    if database.privateVcs.find_one({"owner_id": userId}) is None:
        userInfo = database.getUserData(userId)
        if userInfo["wallet"] > 100:
            database.discordData.find_one_and_update({"discord_id": userId},
                                                     {"$set": {"wallet": (userInfo["wallet"] - 100)}})
            server = client.get_guild(819441557664169994)
            username = ctx.author.name
            roleName = f"{username}'s priv vc"
            channelName = f"{username}'s VC"
            await server.create_role(name=roleName)
            role = get(server.roles, name=roleName)
            user = server.get_member(userId)
            await user.add_roles(role)
            overwrites = {
                server.default_role: discord.PermissionOverwrite(connect=False),
                role: discord.PermissionOverwrite(connect=True)

            }
            await server.create_voice_channel(channelName,
                                              category=discord.utils.get(server.categories,
                                                                         id=PRIVATE_CHANNELS_CATEGORY_ID),
                                              overwrites=overwrites)
            database.createPrivateVc(userId, roleName)
        else:
            await ctx.channel.send("Insufficient funds")
    else:
        await ctx.channel.send("A private vc has already been created")






@client.command(name="test2")
async def upgradeVc(ctx):
    try:
        vcData = database.privateVcs.find_one({"owner_id": ctx.author.id})
        if vcData is None:
            await ctx.send("You dont have a private vc")
        else:
            userInfo = database.getUserData(ctx.author.id, ctx.author.name)
            if vcData["is_upgraded"]:
                await ctx.send("Your private vc is already upgraded")

            elif userInfo["wallet"]<50:
                await ctx.send("Insufficient funds")
            else:
                database.privateVcs.find_one_and_update({"owner_id":ctx.author.id},
                                                        {"$set":{"is_upgraded":True}})
                database.discordData.find_one_and_update({"discord_id":ctx.author.id},
                                                         {"$set":{"wallet":userInfo["wallet"]-50}})
                await ctx.send("Your private vc has been upgraded")
    except Exception as e:
        pass
client.run(token=SECRET_KEY)
