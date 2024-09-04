import discord
from pages.helperFunctions.helperFunctions import *
from pages.pageModel.shopPageModel import shopPages

class ShopPaginationView(discord.ui.View):
    currentPage = 1
    def __init__(self):
        self.shopPagesNum = len(shopPages.keys())
    async def buy(self):
        if self.currentPage == 2:
            await createVc(self.ctx)
        elif self.currentPage == 3:
            await upgradeVc(self.ctx)
        elif self.currentPage == 4:
            await buyPcHour(self.ctx)
        elif self.currentPage == 5:
            await buyFifaMatch(self.ctx)

    async def send(self, ctx):
        self.ctx = ctx
        self.id = self.ctx.author.id

        self.firstButton.disabled = True
        self.previousButton.disabled = True
        self.BuyButton.disabled = True
        self.message = await ctx.send(embed=shopPages[self.currentPage.__str__()], view=self)

    async def updateMessage(self, page):
        await self.message.edit(embed=shopPages[page], view=self)

    def disableButtons(self):
        if self.currentPage == 1:
            self.firstButton.disabled = True
            self.previousButton.disabled = True
            self.BuyButton.disabled = True
            self.LastButton.disabled = False
            self.nextButton.disabled = False

        elif self.currentPage == self.shopPagesNum:
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
            self.currentPage = self.shopPagesNum
            self.disableButtons()
            await self.updateMessage(self.currentPage.__str__())

    @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
    async def BuyButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.id != self.id:
            await interaction.user.send("This embed belongs to another member you cannot interact with it")
        else:
            await self.buy()