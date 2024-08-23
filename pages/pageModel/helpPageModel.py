import discord

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
    description=f'',
    colour=discord.Colour.dark_teal()
)
HelpPage2.add_field(name="/stats", value="Shows how much time a member has spent in Voice Channels")
HelpPage2.add_field(name="/vcLeaderboard",
                    value="Shows the top 10 list of members with the most time spent in Voice Channels")
HelpPage2.add_field(name="/wallet", value="Shows how much points a member has")

HelpPage3 = discord.Embed(
    title="Rewards Criteria      3/5",
    description="""Members get one point for each hour spent in Voice Channels. These points can be used in the shop""",

    colour=discord.Colour.dark_teal()
)
HelpPage3.add_field(name="Note",
                    value="Time spent in the Voice Channel will only be added once the member mutes themselves or "
                          "leaves the Voice Channel")
HelpPage4 = discord.Embed(
    title="Shop      4/5",
    description="Points earned can be used in the shop using the command /shop",
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