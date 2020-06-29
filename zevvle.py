import discord
from discord.ext import commands
import aiohttp
import re

class Zevvle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.zevvleRed = 0xDA291C
        self.zevvleLogo = 'https://zevvle.com/assets/images/social_logo.png'

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Zevvle cog ready")

    @commands.group()
    async def zevvle(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    # Commands
    @zevvle.command()
    async def pricing(self, ctx, *arg):
        if len(arg) == 1:
            async with aiohttp.ClientSession() as session:
                data = await session.get(f"https://api.zevvle.com/pricing/{arg[0]}")
                data = await data.json()
                await session.close()
        if len(arg) == 2:
            async with aiohttp.ClientSession() as session:
                data = await session.get(f"https://api.zevvle.com/pricing/{arg[0]}/{arg[1]}")
                data = await data.json()
                await session.close()
        pricingEmbed = await self.make_pricing_embed(data)
        try:
            await ctx.send(embed=pricingEmbed)
        except Exception as err:
            await ctx.send(embed=discord.Embed(description=err))

    async def make_pricing_embed(self, data):
        sC = re.compile("Pricing within .*") # Single country
        dC = re.compile("Pricing from .* to .*") # Dual country
        nC = re.compile("Country .* doesn't exist.") # No country
        try:
            desc = data['message']
            embed = discord.Embed(colour=self.zevvleRed,description=data['message'])
            embed.set_author(name="Zevvle Pricing", icon_url=self.zevvleLogo)
            return embed
        except KeyError:
            pass
        if dC.match(data['description']):
            embed = discord.Embed(colour=self.zevvleRed,description=data['description'])
            embed.set_author(name="Zevvle Pricing", icon_url=self.zevvleLogo)
            for i in ['voice','sms','mms']:
                embed.add_field(name=i.capitalize(),value=f"£{data[i]/100}",inline=True)
            return embed
        if sC.match(data['description']):
            embed = discord.Embed(colour=self.zevvleRed,description=data['description'])
            embed.set_author(name="Zevvle Pricing", icon_url=self.zevvleLogo)
            for i in data:
                if type(data[i]) is dict:
                    embed.add_field(name="Data Tiers",value="​",inline=False)
                    for x in data[i]:
                        val = []
                        for y in data[i][x]:
                            val.append(y)
                            val.append(data[i][x][y])
                            l = [data[i][x][y] for y in data[i][x]]
                        embed.add_field(name=x,value=f"```{val[0]}: £{val[1]/100}\n{val[2]}: £{val[3]/100}```",inline=True)
                if type(data[i]) is int:
                    embed.add_field(name=i.capitalize(),value=f"£{data[i]/100}",inline=True)
            return embed

def setup(client):
    client.add_cog(Zevvle(client))
