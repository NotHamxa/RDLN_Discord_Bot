import time

from discord import Interaction
from discord._types import ClientT

from database.db import database
import discord.ui


class EmailInputModal(discord.ui.Modal, title="Verify your account"):
    codeInput = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Enter verification code sent to you email",
        required=True,
        max_length=20,
        placeholder="XXXXXX",
    )

    def __init__(self, email, verificationCode, expiration):
        super().__init__()
        self.email = email
        self.verificationCode = verificationCode
        self.expiration = expiration
    async def on_submit(self, interaction: Interaction[ClientT]) -> None:
        if self.expiration < time.time():
            await interaction.response.send_message("Code has expired")
            return
        verificationCode = self.codeInput.value
        if verificationCode != self.verificationCode:
            await interaction.response.send_message("Invalid code! Try again")
            return
        if database.discordData.find_one({"alphaEmail":self.email}) is not None:
            await interaction.response.send_message("Email already in use")
            return
        database.discordData.find_one_and_update({"discord_id": interaction.user.id},
                                                 {"$set": {"alphaEmail": self.email, "isStudent": True}})
        await interaction.response.send_message("Your discord account has been verified. Thank you!")
    async def on_error(self, interaction: Interaction[ClientT], error: Exception) -> None:
        await interaction.response.send_message("something went wrong")

