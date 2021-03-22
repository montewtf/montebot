import discord
from discord.ext import commands
import json
import asyncio
import pokeparty

class Fight(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        
    def cog_check(self, ctx):
        with open("json/fights.json") as f_obj:
            fights = json.load(f_obj)
        return fights.get(str(ctx.author.id)) != None
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You aren't in a battle!")
        
    @commands.command()
    async def fight(self, ctx):
        pass
    
    @commands.command()
    async def run(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        del party["7"]
        parties[str(ctx.author.id)]=party
        with open("json/parties.json", "w") as f_obj:
            json.dump(parties, f_obj, indent=4)
        await ctx.send("Got away safely")
    
def setup(bot):
    bot.add_cog(Fight(bot))