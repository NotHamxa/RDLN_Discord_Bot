import discord
from pages.pageModel.helpPageModel import helpPages


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
