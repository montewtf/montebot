import discord
from discord.ext import commands
import json
import asyncio
import pokeparty
import random
import math

class Fight(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        
    def cog_check(self, ctx):
        with open("json/parties.json") as f_obj:
            fights = json.load(f_obj)
        return fights.get(str(ctx.author.id)).get("7") != None
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You aren't in a battle!")
        
    @commands.command()
    async def fight(self, ctx):
        pass
    
    @commands.command()
    async def pokemon(self, ctx):
        pass
    
    @commands.command()
    async def catch(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        if party.get("6")!=None:
            await ctx.send("Can't have more than 6 pokemon")
            return
        poke = pokeparty.pokemon(poke=party.get("7"))
        r1 = random.randint(0,255)
        if poke.status in ["sleep", "freeze"]:
            s=25
        elif poke.status in ["poison", "burn", "paralysis"]:
            s=12
        else: s=0
        r = r1-s
        f = math.floor(poke.hp*255/12)
        h = math.floor(poke.curhp/4)
        if h==0:h=1
        f = math.floor(f/h)
        if r < 0:
            caught = True
        elif poke.catch < r:
            caught = False
        else:
            r2 = random.randint(0,255)
            if r2<=f:
                caught = True
            else: caught = False
        if caught:
            await ctx.send("wobble...")
            await ctx.send("wobble...")
            await ctx.send("wobble...")
            await ctx.send("Click!")
            await ctx.send("You caught a "+poke.species+"!")
            party = pokeparty.party(party)
            party.add(poke.export())
            party = party.recon()
            parties[str(ctx.author.id)]=party
            with open("json/parties.json", "w") as f_obj:
                json.dump(parties, f_obj, indent=4)
        else:
            w = math.floor(100*poke.catch/255)
            w = math.floor(w*f/255)
            if poke.status in ["sleep", "freeze"]:
                w+=10
            elif poke.status in ["poison", "burn", "paralysis"]:
                w+=5
            if w<10:
                await ctx.send("The ball missed the Pokemon")
            elif w<30:
                await ctx.send("wobble...")
                await ctx.send("Darn! The Pokemon broke free!")
            elif w<70:
                await ctx.send("wobble...")
                await ctx.send("wobble...")
                await ctx.send("Aww! It appeared to be caught!")
            else:
                await ctx.send("wobble...")
                await ctx.send("wobble...")
                await ctx.send("wobble...")
                await ctx.send("Shoot! It was so close too!")
        
    @commands.command()
    async def run(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        speed = party.get("1").get("stats").get("Speed")
        ospeed = party.get("7").get("stats").get("Speed")
        f = speed*32/(ospeed/4)%256+30*party.get("7").get("run")
        g = random.randint(0,255)
        if f>g:
            del party["7"]
            parties[str(ctx.author.id)]=party
            with open("json/parties.json", "w") as f_obj:
                json.dump(parties, f_obj, indent=4)
            await ctx.send("Got away safely")
        else:
            party.get("7")["run"] +=1
            parties[str(ctx.author.id)]=party
            with open("json/parties.json", "w") as f_obj:
                json.dump(parties, f_obj, indent=4)
            await ctx.send("Can't escape")
    
def setup(bot):
    bot.add_cog(Fight(bot))