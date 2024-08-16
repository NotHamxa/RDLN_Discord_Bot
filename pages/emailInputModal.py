import discord.ui


class EmailInputModal(discord.ui.Modal,title="Verify your account"):
    emailInput = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Enter verification code sent to you email",
        required=True,
        max_length=20,
        placeholder="E",
    )
    async def on_submit(self, interaction:discord.Interaction):
        print(self.emailInput.value)
