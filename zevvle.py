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
        await ctx.send(embed=pricingEmbed)

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
                embed.add_field(name=i.capitalize(),value=data[i],inline=True)
            return embed
        if sC.match(data['description']):
            embed = discord.Embed(colour=self.zevvleRed,description=data['description'])
            embed.set_author(name="Zevvle Pricing", icon_url=self.zevvleLogo)
            for i in ['megabyte', 'gigabyte', 'sms', 'mms', 'voice', 'voicemail', 'incoming']:
                embed.add_field(name=i.capitalize(),value=f"£{data[i]/100}",inline=True)
            embed.add_field(name="Data Tiers",value="",inline=False)
            for i in data['data_tiers']:
                n = [i for i in data['data_tiers'][x]]
                l = [data['data_tiers'][x][i] for i in data['data_tiers'][x]]
                embed.add_field(name=i,value=f"```{n[0].capitalize()}: £{l[0]}\n{n[1].capitalize()}: £{l[1]}```",inline=True)
            return embed

def setup(client):
    client.add_cog(Zevvle(client))
