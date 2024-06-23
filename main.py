import discord
from discord.ext import commands, tasks
from discord.utils import get
import time
from db import database
import os
SECRET_KEY = os.getenv('SECRET_KEY')
BOT_ANNOUNCEMENTS_CHANNEL_ID = 1178684719144128533
PRIVATE_CHANNELS_CATEGORY_ID = 1190401067813453984
GENERAL_CHANNEL_ID = 1157024450504560651
SERVER_ID = 819441557664169994
MY_ID = 829376179706134558
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="rdln.", intents=intents, help_command=None)


@client.event
async def on_ready():
    try:
        x = await client.tree.sync()
        print(f'{x} commands synced')
    except Exception as e:
        print(e)



@client.command(name="selfDestruct")
async def selfDestruct(ctx):
    try:
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            return
        else:
            if ctx.author.id != 829376179706134558:
                await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
            else:
                await ctx.send("Wiping BOT Data")
                await ctx.send("BOT Closed")
                exit()
    except Exception as e:
        print(e)


accs = {}
muted = []
shopStatus = True
HelpPage1 = discord.Embed(
    title="Help      1/5",
    description="""
Page2 : Commands
Page3 : Rewards Criteria
Page4 : Shop
Page5 : Private Voice Channel
""",
    colour=discord.Colour.dark_teal())
HelpPage2 = discord.Embed(
    title="Commands      2/5",
    description=f'all commands will start with the prefix "rdln."',
    colour=discord.Colour.dark_teal()
)
HelpPage2.add_field(name="stats", value="Shows how much time a member has spent in Voice Channels")
HelpPage2.add_field(name="vcLeaderboard",
                    value="Shows the top 10 list of members with the most time spent in Voice Channels")
HelpPage2.add_field(name="wallet", value="Shows how much points a member has")

HelpPage3 = discord.Embed(
    title="Rewards Criteria      3/5",
    description="""Members get one point for each hour spent in Voice Channels. These points can be used in the shop""",

    colour=discord.Colour.dark_teal()
)
HelpPage3.add_field(name="Note",
                    value="Time spent in the Voice Channel will only be added once the member mutes themselves or leaves the Voice Channel")
HelpPage4 = discord.Embed(
    title="Shop      4/5",
    description="Points earned can be used in the shop using the command prefix rdln.shop",
    colour=discord.Colour.dark_teal()
)
HelpPage4.add_field(name="Private VC", value="""
Buy a private voice channel for you and your friends. Limited to 5 additional users.
Price: 100 points
""")
HelpPage4.add_field(name="Private VC Upgrade", value="""
Upgrade your existing private vc to remove the user limitation.
Price: 50 points
""")
HelpPage5 = discord.Embed(title="Private Voice Channel      5/5", description="""
All of the commands related to the private voice channels  starting with the prefix .
""")
HelpPage5.add_field(name="rdln.addUser <username>", value="""
Give access to a user by this command.
For ex:
rdln.addUser nothamxa""")
HelpPage5.add_field(name="rdln.removeUser <username>", value="""
Remove access from a user by this command.
For ex:
rdln.removeUser nothamxa""")
HelpPage5.add_field(name="rdln.vcUsers", value="""
Shows the users who have access to your private channel.
""")
helpPages = {"1": HelpPage1, "2": HelpPage2, "3": HelpPage3, "4": HelpPage4, "5": HelpPage5}


class HelpPaginationView(discord.ui.View):
    currentPage = 1

    async def send(self, ctx):
        self.firstButton.disabled = True
        self.previousButton.disabled = True
        self.message = await ctx.send(embed=helpPages[self.currentPage.__str__()], view=self)
        self.id = ctx.author.id

    async def updateMessage(self, page):
        await self.message.edit(embed=helpPages[page], view=self)

    def disableButtons(self):
        if self.currentPage == 1:
            self.firstButton.disabled = True
            self.previousButton.disabled = True
            self.LastButton.disabled = False
            self.nextButton.disabled = False
        elif self.currentPage == 5:
            self.LastButton.disabled = True
            self.nextButton.disabled = True
            self.firstButton.disabled = False
            self.previousButton.disabled = False
        else:
            self.firstButton.disabled = False
            self.previousButton.disabled = False
            self.LastButton.disabled = False
            self.nextButton.disabled = False

    @discord.ui.button(label="|<", style=discord.ButtonStyle.primary)
    async def firstButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:

            self.currentPage = 1
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def previousButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage -= 1
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def nextButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage += 1
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label=">|", style=discord.ButtonStyle.primary)
    async def LastButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage = 5
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())


ShopPage1 = discord.Embed(
    title="Shop      1/3",
    description="""
Page2 : Private Voice Channel
Page3 : Private Voice Channel(Upgrade)
""",
    colour=discord.Colour.dark_teal())

ShopPage2 = discord.Embed(
    title="Private VC      2/3",
    description=""" Buy to receive a private voice channel.
Voice channel will be limited to 5 users excluding you. 
For details regarding this go to rdln.help.

Price: 100 Points.
""",
    colour=discord.Colour.dark_teal()
)
ShopPage3 = discord.Embed(
    title="Private VC Upgrade      3/3",
    description="""Buy to upgrade your private voice channel.
This will allow you to add as many friends as you want.

Price: 50 Points.
""",
    colour=discord.Colour.dark_teal()
)
ShopPages = {"1": ShopPage1, "2": ShopPage2, "3": ShopPage3}


class ShopPaginationView(discord.ui.View):
    currentPage = 1

    async def buy(self):
        data = database.getUserData(self.id, self.ctx.author.name)
        if self.currentPage == 2:
            await createVc(self.ctx)
        elif self.currentPage == 3:
            await upgradeVc(self.ctx)

    async def send(self, ctx):
        self.ctx = ctx
        self.id = self.ctx.author.id

        self.firstButton.disabled = True
        self.previousButton.disabled = True
        self.BuyButton.disabled = True
        self.message = await ctx.send(embed=ShopPages[self.currentPage.__str__()], view=self)

    async def updateMessage(self, page):
        await self.message.edit(embed=ShopPages[page], view=self)

    def disableButtons(self):
        if self.currentPage == 1:
            self.firstButton.disabled = True
            self.previousButton.disabled = True
            self.BuyButton.disabled = True
            self.LastButton.disabled = False
            self.nextButton.disabled = False

        elif self.currentPage == 3:
            self.LastButton.disabled = True
            self.nextButton.disabled = True
            self.firstButton.disabled = False
            self.previousButton.disabled = False
            self.BuyButton.disabled = False
        else:
            self.firstButton.disabled = False
            self.previousButton.disabled = False
            self.LastButton.disabled = False
            self.nextButton.disabled = False
            self.BuyButton.disabled = False

    @discord.ui.button(label="|<", style=discord.ButtonStyle.primary)
    async def firstButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage = 1
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def previousButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage -= 1
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def nextButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage += 1
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label=">|", style=discord.ButtonStyle.primary)
    async def LastButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            self.currentPage = 3
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
    async def BuyButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            await self.buy()


@client.tree.command(name="shop")
async def shop(ctx):
    try:
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            if not shopStatus:
                await ctx.channel.send("Shop is currently disabled")
            else:
                paginationView = ShopPaginationView()

                await paginationView.send(ctx)
    except Exception as e:
        print(e)


@client.command(name="help")
async def help(ctx):
    try:
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            paginationView = HelpPaginationView()

            await paginationView.send(ctx)
    except Exception as e:
        print(e)


@client.command(name="vcLeaderboard")
async def learderBoard(ctx):
    try:
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            data = database.TopTen()
            description = ""
            try:
                title = "TOP 10"
                first = f'01 - 🥇 {client.get_user(data[0]["discord_id"]).name} with {database.cnvrtTime(data[0]["discord_time"])}'
                second = f'02 - 🥈 {client.get_user(data[1]["discord_id"]).name} with {database.cnvrtTime(data[1]["discord_time"])}'
                third = f'03 - 🥉 {client.get_user(data[2]["discord_id"]).name} with {database.cnvrtTime(data[2]["discord_time"])}'
                top3 = first + "\n" + second + "\n" + third + "\n"
            except:
                title = "Not enough people to make a leaderboard"

            try:
                for i in range(3, len(data)):
                    name = client.get_user(data[i]["discord_id"]).name
                    if i != 9:
                        x = "0" + str(i + 1)
                    else:
                        x = "10"
                    description += f'{x} - 🏅 {name} with {database.cnvrtTime(data[i]["discord_time"])}'
                    description += "\n"
            except:
                description = ""
            embed = discord.Embed(
                colour=discord.Colour.dark_teal(),
                title=title,
                description=top3 + description
            )
            embed.set_thumbnail(url=client.get_user(data[0]["discord_id"]).display_avatar)
            embed.set_author(name="VC Leaderboard")

            await ctx.channel.send(embed=embed)
    except Exception as e:
        print(e)


@client.command(name="stats")
async def my_stats(ctx):
    try:

        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            id = ctx.message.author.id
            name = ctx.message.author.name
            data = database.getUserData(id, name)

            if data != None:
                hrs = int((data["discord_time"] // 3600))
                mins = int((data["discord_time"] - (hrs * 3600)) // 60)
                embed = discord.Embed(
                    colour=discord.Colour.dark_teal(),
                    description=f'''
You have spent {hrs}hrs {mins}mins on the Redline Server''')
                embed.set_author(name=f"{name}")
                embed.add_field(name="Help", value="For more information use the command rdln.help")
                embed.set_thumbnail(url=ctx.message.author.display_avatar)
                await ctx.channel.send(embed=embed)

    except Exception as e:
        print(e)


@client.event
async def on_voice_state_update(member, before, after):
    try:

        if ((before.channel is None and after.channel is not None) or (
                before.channel is not None and after.channel is not None)):
            if member.id not in accs:
                data = database.getUserData(member.id, member.name)
                accs.update({member.id: {"name": member, "time": data["discord_time"], "temp_time": time.time_ns()}})

        if after.channel is not None:
            if after.self_mute == True and member.id not in muted:
                if accs[member.id]["temp_time"] != 0:
                    accs[member.id]["time"] += int((time.time_ns() - accs[member.id]["temp_time"]) / 1000000000)
                    database.setTime(member.id, accs[member.id]["time"])

                    database.setCode(member.id)

                    muted.append(member.id)

            elif after.self_mute == False and member.id in muted:

                muted.remove(member.id)
                accs[member.id]["temp_time"] = time.time_ns()



        elif before.channel is not None and after.channel is None:
            if accs.get(member.id) != None:
                if member.id not in muted:
                    if accs[member.id]["temp_time"] != 0:
                        accs[member.id]["time"] += int((time.time_ns() - accs[member.id]["temp_time"]) / 1000000000)
                        database.setTime(member.id, accs[member.id]["time"])

                        database.setCode(member.id)

                        del accs[member.id]
                        if member.id in muted:
                            muted.remove(member.id)

    except Exception as e:
        print(e)


@client.command(name="wallet")
async def wallet(ctx):
    try:

        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            data = database.getUserData(ctx.author.id, ctx.author.name)
            await ctx.send(f'You have {data["wallet"]} point(s) in your wallet')

    except Exception as e:
        print(e)


@client.command(name="codeStatus")
async def verifyCode(ctx, arg=None):
    try:

        if ctx.message.channel.id != 1175788361651339416 or arg == None:
            return
        else:
            data = database.verifyCode(arg, False)
            if data is None:
                await ctx.send("Incorrect Code")

            else:
                if not data["used"]:
                    status = "not used"
                else:
                    status = "used"
                response = f"""
Status: {status}
Given For: {data["usedFor"]}
                """
            await ctx.send(response)

    except Exception as e:
        print(e)


@client.command(name="useCode")
async def useCode(ctx, arg=None):
    try:

        if ctx.channel.id not in [1157041206572892169, 1167100338914988112] or arg == None:
            return
        else:
            data = database.useCode(arg)
            if not data["present"]:
                await ctx.message.channel.send("Incorrect Code")
            elif data["success"]:
                await ctx.message.channel.send("Code successfully Used")
            elif not data["success"]:
                await ctx.message.channel.send("Code Already Used")

    except Exception as e:
        print(e)


@client.command(name="setShopStatus")
async def setStatus(ctx, arg=None):
    try:

        global shopStatus

        if ctx.channel.id not in [1157041206572892169, 1167100338914988112] or arg == None:
            return
        else:
            if ctx.author.id != 829376179706134558:
                await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
            else:

                if str(arg).lower() == "open":
                    shopStatus = True
                    await ctx.channel.send("Shop Opened")
                elif str(arg).lower() == "close":
                    await ctx.channel.send("Shop Closed")
                    shopStatus = False

    except Exception as e:
        print(e)


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
                                                                             id=PRIVATE_CHANNELS_CATEGORY_ID),
                                                  overwrites=overwrites)
                database.createPrivateVc(userId, roleName)
                general = client.get_channel(GENERAL_CHANNEL_ID)
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
                general = client.get_channel(GENERAL_CHANNEL_ID)
                await general.send(f"{user.mention} upgraded their private voice channel from the Redline Shop")
    except Exception as e:

        print(e)


@client.command(name="addUser")
async def addUser(ctx, arg=None):
    try:
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            server = client.get_guild(819441557664169994)
            userId = ctx.author.id
            vcData = database.privateVcs.find_one({"owner_id": userId})
            if vcData is not None:
                if vcData["people_num"] == 5 and not vcData["is_upgraded"]:
                    await ctx.send(
                        "Maximum number of users reached. To add new users upgrade the current vc using rdln.vcUpgrade")
                    return
                else:
                    try:

                        user = str(arg)
                        member = get(server.members, name=user)
                        if member is None:
                            await ctx.send("Member does not exist")
                        elif member.name == ctx.author.name:
                            await ctx.send("You cannot add yourself to the vc")
                        elif vcData["people"] is not None and member.id in vcData["people"]:
                            await ctx.send("User already has access to the vc")
                        else:
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
                    except Exception as e:
                        print(e)

            else:
                await ctx.channel.send("You do not own a private vc!")
    except Exception as e:
        print(e)


@client.command(name="vcUsers")
async def vcUserList(ctx):
    try:
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            await ctx.channel.send("Commands can only be sent in the bot commands channel")
        else:
            vcData = database.privateVcs.find_one({"owner_id": ctx.author.id})
            if vcData is None:
                await ctx.send("You dont have a private vc")
            else:

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
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
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
        if ctx.channel.id not in [1157041206572892169, 1167100338914988112]:
            return
        else:
            if ctx.author.id != MY_ID:
                await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
            else:
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
        else:
            if ctx.author.id != MY_ID:
                return
            else:
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


client.run(token=SECRET_KEY)
