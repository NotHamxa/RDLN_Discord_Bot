import discord

from database.db import database
from models.config import configuration, currentConfiguration
from models.models import User
from pages.helpPage import HelpPaginationView
from pages.shopPage import ShopPaginationView


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
    if ctx.channel.id not in configuration.mainBotChannels:
        await ctx.channel.send("Commands can only be sent in the bot commands channel")
        return

    id = ctx.message.author.id
    name = ctx.message.author.name
    data:User = database.getUserData(id, name)

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

    data = database.getUserData(ctx.author.id, ctx.author.name)
    await ctx.send(f'You have {data["wallet"]} point(s) in your wallet')

