import discord
from discord.utils import get
from database.db import database

from models.config import configuration
async def createVc(ctx):
    try:

        userId = ctx.author.id
        if database.privateVcs.find_one({"owner_id": userId}) is None:
            userInfo = database.getUserData(userId)
            if userInfo["wallet"] >= 100:
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
                                                                             id=configuration.privateChannelsCategoryId),
                                                  overwrites=overwrites)
                database.createPrivateVc(userId, roleName)
                general = client.get_channel(configuration.generalChannelId)
                await general.send(f"{user.mention} bought a private voice channel from the Redline Shop")
            else:
                await ctx.channel.send("Insufficient funds")
        else:
            await ctx.channel.send("A private vc has already been created")
    except Exception as e:
        print(e)


async def upgradeVc(ctx):
    try:

        vcData = database.privateVcs.find_one({"owner_id": ctx.author.id})
        if vcData is None:
            await ctx.send("You dont have a private vc")
        else:
            userInfo = database.getUserData(ctx.author.id, ctx.author.name)
            if vcData["is_upgraded"]:
                await ctx.send("Your private vc is already upgraded")

            elif userInfo["wallet"] < 50:
                await ctx.send("Insufficient funds")
            else:
                database.privateVcs.find_one_and_update({"owner_id": ctx.author.id},
                                                        {"$set": {"is_upgraded": True}})
                database.discordData.find_one_and_update({"discord_id": ctx.author.id},
                                                         {"$set": {"wallet": userInfo["wallet"] - 50}})
                user = client.get_user(ctx.author.id)
                general = client.get_channel(configuration.generalChannelId)
                await general.send(f"{user.mention} upgraded their private voice channel from the Redline Shop")
    except Exception as e:

        print(e)
