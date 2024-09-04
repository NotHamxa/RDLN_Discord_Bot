import discord

ShopPage1 = discord.Embed(
    title="Shop      1/5",
    description="""
Page2 : Private Voice Channel
Page3 : Private Voice Channel(Upgrade)
Page4 : RDLN PC(1 Hour)
Page5 : FIFA 1 Match
""",
    colour=discord.Colour.dark_teal())

ShopPage2 = discord.Embed(
    title="Private VC      2/5",
    description="""Buy to receive a private voice channel.
Voice channel will be limited to 5 users excluding you. 
For details regarding this go to rdln.help.

Price: 100 Points.
""",
    colour=discord.Colour.dark_teal()
)
ShopPage3 = discord.Embed(
    title="Private VC Upgrade      3/5",
    description="""Buy to upgrade your private voice channel.
This will allow you to add as many friends as you want.

Price: 50 Points.
""",
    colour=discord.Colour.dark_teal()
)
ShopPage4 = discord.Embed(
    title="RDLN PC(1 Hour)      4/5",
    description="""Buy to redeem 1 hour of pc.
Buy to receive a code which can be redeemed for 1 hour of pc.

Price: 50 Points.

Note: Your discord account needs to be verified with your alpha email.
To verify your account use /verify.
""",
    colour=
    discord.Colour.dark_teal()
)
ShopPage5 = discord.Embed(
    title="FIFA 1 Match      5/5",
    description="""Buy to receive a code which can be redeemed for 1 FIFA Match

Price: 50 Points.

Note: Your discord account needs to be verified with your alpha email.
To verify your account use /verify.
""",
    colour=discord.Colour.dark_teal()
)
shopPages = {"1": ShopPage1, "2": ShopPage2, "3": ShopPage3,"4": ShopPage4, "5": ShopPage5}

