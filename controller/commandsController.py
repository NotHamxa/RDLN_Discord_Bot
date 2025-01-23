import random
import string
import time
from threading import Thread
import discord
from discord.utils import get
from discord.ext.commands.context import Context
from database.db import database
from models.config import configuration, currentConfiguration
from models.models import User, EmailVerificationModel
from pages.helpPage import HelpPaginationView
from pages.shopPage import ShopPaginationView
from pages.emailInputModal import EmailInputModal
from mail.mail import sendVerificationMail

async def selfDestruct(ctx):
    """
    Function for closing the bot
    :param ctx:
    :return:
    """
    if ctx.channel.id not in configuration.mainBotChannels:
        return
    if ctx.author.id not in configuration.mainAdminIds:
        await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
        return
    await ctx.send("Wiping BOT Data")
    await ctx.send("BOT Closed")
    exit()


async def shop(interaction: discord.Interaction):
    """
    Sends the shop page in the case that shop is open
    :param ctx:
    :return:
    """
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return
    if not currentConfiguration.shopStatus:
        await ctx.channel.send("Shop is currently disabled")
        return
    paginationView = ShopPaginationView()
    await paginationView.send(ctx)


async def help(interaction:discord.Interaction):
    """
    Sends the help page
    :param ctx:
    :return:
    """
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return
    paginationView = HelpPaginationView()
    await paginationView.send(ctx)


async def vcLeaderboard(interaction:discord.Interaction):
    """
    Checks and sends the list of the top ten users on the basis of time spent in voice channels
    At least 3 users have to be in the database to send the leaderboard
    :param ctx:
    :return:
    """
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return
    data = database.TopTen()
    description = ""
    top3 = ""
    # checking if there are a minimum of 3 users in the database
    try:
        title = "TOP 10"
        first = f'01 - 🥇 {currentConfiguration.client.get_user(data[0]["discord_id"]).name} with {database.cnvrtTime(data[0]["discord_time"])}'
        second = f'02 - 🥈 {currentConfiguration.client.get_user(data[1]["discord_id"]).name} with {database.cnvrtTime(data[1]["discord_time"])}'
        third = f'03 - 🥉 {currentConfiguration.client.get_user(data[2]["discord_id"]).name} with {database.cnvrtTime(data[2]["discord_time"])}'
        top3 = first + "\n" + second + "\n" + third + "\n"
    except Exception as e:
        title = "Not enough people to make a leaderboard"

    # Filling out the rest of the leaderboard
    try:
        for i in range(3, len(data)):
            name = currentConfiguration.client.get_user(data[i]["discord_id"]).name
            if i != 9:
                x = "0" + str(i + 1)
            else:
                x = "10"
            description += f'{x} - 🏅 {name} with {database.cnvrtTime(data[i]["discord_time"])}'
            description += "\n"
    except Exception as e:
        description = ""

    # Configuring an embed to send
    embed = discord.Embed(
        colour=discord.Colour.dark_teal(),
        title=title,
        description=top3 + description
    )
    embed.set_thumbnail(url=currentConfiguration.client.get_user(data[0]["discord_id"]).display_avatar)
    embed.set_author(name="VC Leaderboard")

    await interaction.response.send_message(embed=embed)


async def stats(interaction:discord.Interaction):
    """
    Retrieves the current time for the member calling the function
    In the event that the user does not have a profile in the database a base profile will be set
    :param ctx:
    :return:
    """
    ctx = await Context.from_interaction(interaction)
    print(type(ctx))
    if ctx.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return

    id = ctx.message.author.id
    name = ctx.message.author.name
    data: User = database.getUserData(id, name)

    if data is not None:
        hrs = int((data.discord_time // 3600))
        mins = int((data.discord_time - (hrs * 3600)) // 60)
        embed = discord.Embed(
            colour=discord.Colour.dark_teal(),
            description=f'You have spent {hrs}hrs {mins}mins on the Redline Server')
        embed.set_author(name=f"{name}")
        embed.add_field(name="Help", value="For more information use the command rdln.help")
        embed.set_thumbnail(url=ctx.message.author.display_avatar)
        await interaction.response.send_message(embed=embed)


async def wallet(interaction:discord.Interaction):
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return

    data: User = database.getUserData(ctx.author.id, ctx.author.name)
    await interaction.response.send_message(f'You have {data.wallet} point(s) in your wallet')


# async def verifyCode(ctx,arg):
#     if ctx.message.channel.id != 1175788361651339416 or arg is None:
#         return
#     else:
#         data = database.verifyCode(arg, False)
#         if data is None:
#             await interaction.response.send_message("Incorrect Code")
#
#         else:
#             if not data["used"]:
#                 status = "not used"
#             else:
#                 status = "used"
#             response = f"""
#     Status: {status}
#     Given For: {data["usedFor"]}
#                     """
#         await interaction.response.send_message(response)

# async def useCode(ctx,arg):
#     if ctx.channel.id not in mainBotChannels or arg is None:
#         return
#
#     data = database.useCode(arg)
#     if not data["present"]:
#         await ctx.message.channel.send("Incorrect Code")
#     elif data["success"]:
#         await ctx.message.channel.send("Code successfully Used")
#     elif not data["success"]:
#         await ctx.message.channel.send("Code Already Used")


async def setShopStatus(interaction:discord.Interaction, status):
    """
    change the shop status to either be open or closed.
    Only available to main admin accounts
    :param interaction:
    :param ctx:
    :param arg:
    :return:
    """
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels or status is None:
        return

    if ctx.author.id not in configuration.mainAdminIds:
        await interaction.response.send_message("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
        return

    if str(status).lower() == "open":
        currentConfiguration.shopStatus = True
        await interaction.response.send_message("Shop Opened")
    elif str(status).lower() == "close":
        currentConfiguration.shopStatus = False
        await interaction.response.send_message("Shop Closed")


async def addUser(interaction:discord.Interaction,username):
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return

    server = currentConfiguration.client.get_guild(819441557664169994)
    userId = ctx.author.id
    vcData = database.privateVcs.find_one({"owner_id": userId})
    if vcData is None:
        await interaction.response.send_message("You do not own a private vc!")
        return

    if vcData["people_num"] == 5 and not vcData["is_upgraded"]:
        await interaction.response.send_message(
            "Maximum number of users reached. To add new users upgrade the current vc using rdln.vcUpgrade")
        return

    user = str(username)
    member = get(server.members, name=user)
    if member is None:
        await interaction.response.send_message("Member does not exist")
        return
    if member.id == ctx.author.id:
        await interaction.response.send_message("You cannot add yourself to the vc")
        return
    if vcData["people"] is not None and member.id in vcData["people"]:
        await interaction.response.send_message("User already has access to the vc")
        return

    role = get(server.roles, name=vcData["role_id"])
    await member.add_roles(role)
    if vcData["people"] is None:
        peopleList = [member.id]
    else:
        peopleList = [member.id] + vcData["people"]
    database.privateVcs.find_one_and_update({"owner_id": userId},
                                            {"$set": {"people_num": (vcData["people_num"] + 1),
                                                      "people": peopleList}})
    await interaction.response.send_message("User added")


async def vcUsersList(interaction:discord.Interaction):
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return

    vcData = database.privateVcs.find_one({"owner_id": ctx.author.id})
    if vcData is None:
        await interaction.response.send_message("You dont have a private vc")
        return
    members = ""
    for user in vcData["people"]:
        try:
            member = currentConfiguration.client.get_user(user)
            members += member.name
            members += '\n'
        except Exception as e:
            pass
    embed = discord.Embed(title=f"{ctx.author.name}'s private VC",
                          colour=discord.Colour.dark_teal(),
                          description=members)
    await interaction.response.send_message(embed=embed)


async def removeUser(interaction:discord.Interaction, username):
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return

    server = currentConfiguration.client.get_guild(819441557664169994)
    userId = ctx.author.id
    vcData = database.privateVcs.find_one({"owner_id": userId})
    print(vcData)
    if vcData is None:
        await interaction.response.send_message("You do not own a private vc!")
        return
    member = get(server.members, name=str(username))

    if member is None:
        await interaction.response.send_message("User does not exists")
    elif member.name == ctx.author.name:
        await interaction.response.send_message("You cannot remove yourself from the vc")
    elif vcData["people"] is None or (member.id not in vcData["people"]):
        await interaction.response.send_message("User already doesnt have access to your vc")
    else:
        role = get(server.roles, name=vcData["role_id"])
        await member.remove_roles(role)
        vcData["people"].remove(member.id)
        print(vcData["people"])
        database.privateVcs.find_one_and_update({"owner_id": userId},
                                                {"$set": {"people": vcData["people"],
                                                          "people_num": vcData["people_num"] - 1}})

        await interaction.response.send_message("User removed")


async def addPoints(interaction:discord.Interaction, username,points):
    ctx = await Context.from_interaction(interaction)
    if ctx.channel.id not in configuration.mainBotChannels:
        return
    if ctx.author.id not in configuration.mainAdminIds:
        await interaction.response.send_message("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na "
                                                "Sehta")
        return

    server = currentConfiguration.client.get_guild(configuration.serverId)
    user = get(server.members, name=username)
    if user is not None:
        userData: User = database.getUserData(user.id, user.name)
        database.discordData.find_one_and_update({"discord_id": user.id},
                                                 {"$set": {"wallet": userData.wallet + int(points)}})
    await interaction.response.send_message("Points added")


async def verifyAccount(interaction: discord.Interaction, email: str):
    if interaction.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return
    if database.discordData.find_one({"discord_id": interaction.user.id})["isStudent"]:
        await interaction.response.send_message("Your account is already verified")
        return
    if not email.endswith("@alpha.edu.pk"):
        await interaction.response.send_message("Invalid email")
        return
    if database.discordData.find_one({"alphaEmail":email}) is not None:
        await interaction.response.send_message("Email already in use")
        return
    verificationCode = ''.join(random.choices(string.hexdigits, k=6))
    emailVerificationObj = EmailVerificationModel(**{"discord_id": interaction.user.id,
                                                     "email": email,
                                                     "verificationCode": verificationCode,
                                                     "expiration":int(time.time()) + 500})
    thread = Thread(target=sendVerificationMail,args=("Discord Verification Code",
                                                      email,
                                                      {"CODE": verificationCode}))
    thread.start()
    emailInput = EmailInputModal(emailVerificationObj.email,
                                 emailVerificationObj.verificationCode,
                                 emailVerificationObj.expiration)
    await interaction.response.send_modal(emailInput)


async def clearDB(interaction: discord.Interaction):
    if interaction.channel.id not in configuration.mainBotChannels:
        await interaction.response.send_message("Commands can only be sent in the bot commands channel")
        return
    if interaction.user.id not in configuration.mainAdminIds:
        await interaction.response.send_message("User not authorized")
        return
    database.discordData.delete_many({})
    await interaction.channel.send("Deleted all user profiles")
    database.discordCodes.delete_many({})
    await interaction.channel.send("Deleted all existing codes")
