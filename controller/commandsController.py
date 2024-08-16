import discord
from discord.utils import get

from database.db import database
from models.config import configuration, currentConfiguration
from models.models import User
from pages.helpPage import HelpPaginationView
from pages.shopPage import ShopPaginationView
from pages.emailInputModal import EmailInputModal


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


async def shop(ctx):
    """
    Sends the shop page in the case that shop is open
    :param ctx:
    :return:
    """
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return
    if not currentConfiguration.shopStatus:
        await ctx.channel.send("Shop is currently disabled")
        return
    paginationView = ShopPaginationView()
    await paginationView.send(ctx)


async def help(ctx):
    """
    Sends the help page
    :param ctx:
    :return:
    """
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return
    paginationView = HelpPaginationView()
    await paginationView.send(ctx)


async def vcLeaderboard(ctx):
    """
    Checks and sends the list of the top ten users on the basis of time spent in voice channels
    At least 3 users have to be in the database to send the leaderboard
    :param ctx:
    :return:
    """
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

    await ctx.channel.send(embed=embed)


async def stats(ctx):
    """
    Retrieves the current time for the member calling the function
    In the event that the user does not have a profile in the database a base profile will be set
    :param ctx:
    :return:
    """
    print(type(ctx))
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
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
        await ctx.channel.send(embed=embed)


async def wallet(ctx):
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return

    data: User = database.getUserData(ctx.author.id, ctx.author.name)
    await ctx.send(f'You have {data.wallet} point(s) in your wallet')


# async def verifyCode(ctx,arg):
#     if ctx.message.channel.id != 1175788361651339416 or arg is None:
#         return
#     else:
#         data = database.verifyCode(arg, False)
#         if data is None:
#             await ctx.send("Incorrect Code")
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
#         await ctx.send(response)

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


async def setShopStatus(ctx, arg):
    """
    change the shop status to either be open or closed.
    Only available to main admin accounts
    :param ctx:
    :param arg:
    :return:
    """
    if ctx.channel.id not in configuration.mainBotChannels or arg is None:
        return

    if ctx.author.id not in configuration.mainAdminIds:
        await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
        return

    if str(arg).lower() == "open":
        currentConfiguration.shopStatus = True
        await ctx.channel.send("Shop Opened")
    elif str(arg).lower() == "close":
        currentConfiguration.shopStatus = False
        await ctx.channel.send("Shop Closed")


async def addUser(ctx, arg):
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return

    server = currentConfiguration.client.get_guild(819441557664169994)
    userId = ctx.author.id
    vcData = database.privateVcs.find_one({"owner_id": userId})
    if vcData is None:
        await ctx.channel.send("You do not own a private vc!")
        return

    if vcData["people_num"] == 5 and not vcData["is_upgraded"]:
        await ctx.send(
            "Maximum number of users reached. To add new users upgrade the current vc using rdln.vcUpgrade")
        return

    user = str(arg)
    member = get(server.members, name=user)
    if member is None:
        await ctx.send("Member does not exist")
        return
    if member.id == ctx.author.id:
        await ctx.send("You cannot add yourself to the vc")
        return
    if vcData["people"] is not None and member.id in vcData["people"]:
        await ctx.send("User already has access to the vc")
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
    await ctx.send("User added")


async def vcUsersList(ctx):
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return

    vcData = database.privateVcs.find_one({"owner_id": ctx.author.id})
    if vcData is None:
        await ctx.send("You dont have a private vc")
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
    await ctx.send(embed=embed)


async def removeUser(ctx, arg):
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return

    server = currentConfiguration.client.get_guild(819441557664169994)
    userId = ctx.author.id
    vcData = database.privateVcs.find_one({"owner_id": userId})
    if vcData is None:
        await ctx.channel.send("You do not own a private vc!")
        return
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


async def addPoints(ctx, arg):
    if ctx.channel.id not in configuration.mainBotChannels:
        return
    if ctx.author.id not in configuration.mainAdminIds:
        await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
        return
    arg = str(arg).split(",")
    server = currentConfiguration.client.get_guild(configuration.serverId)
    user = get(server.members, name=arg[0])
    if user is not None:
        userData: User = database.getUserData(user.id, user.name)
        database.discordData.find_one_and_update({"discord_id": user.id},
                                                 {"$set": {"wallet": userData.wallet + int(arg[1])}})
    await ctx.send("Points added")


async def verifyAccount(interaction:discord.Interaction,email:str):
    if not email.endswith("@alpha.edu.pk"):
        await interaction.response.send_message("Invalid email")

    emailInput = EmailInputModal()
    await interaction.response.send_modal(emailInput)
