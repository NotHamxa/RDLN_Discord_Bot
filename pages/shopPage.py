import discord
from database.db import database

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