import discord
from discord.ext import commands
from discord.utils import get

SECRET_KEY = "MTE2NjgxNTMzNzM4NDI2MzgzMA.G20Jyo.lAOSXqeJNgwQRXFC49JEPqgEp5T0F1CWG9-JdA"
BOT_ANNOUNCEMENTS_CHANNEL_ID = 1178684719144128533
PRIVATE_CHANNELS_CATEGORY_ID = 1190401067813453984
GENERAL_CHANNEL_ID = 1157024450504560651
SERVER_ID = 819441557664169994
MY_ID = 829376179706134558
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="rdln.", intents=intents, help_command=None)


@client.command(name="roles")
async def mew(ctx):
    server = client.get_guild(819441557664169994)
    roles = get(server.roles,name="👑 President")
    self = get(server.members,name="nothamxa")
    await self.add_roles(roles)

client.run(SECRET_KEY)