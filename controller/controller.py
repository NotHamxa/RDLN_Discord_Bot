from models.config import configuration


async def selfDestruct(ctx):
    if ctx.channel.id not in configuration.mainBotChannels:
        return
    if ctx.author.id not in configuration.mainAdminIds:
        await ctx.send("L + U thought + U Cant + Dont have the perms + Skill Issue + Me Na Sehta")
        return
    await ctx.send("Wiping BOT Data")
    await ctx.send("BOT Closed")
    exit()