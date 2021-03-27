import discord
from discord.ext import commands
import json
import asyncio
import random
import math
import pokeparty

class Fight(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        
    def cog_check(self, ctx):
        with open("json/parties.json") as f_obj:
            fights = json.load(f_obj)
        return fights.get(str(ctx.author.id)).get("7") != None
    
    def battleBox(self, party):
        battle=pokeparty.pokemon(poke=party.get("7"))
        file=discord.File("thumbnails/"+battle.id+".png", filename="image.png")
        embed=discord.Embed(title=battle.species+" Lv."+str(battle.level), description=str(battle.curhp)+"/"+str(battle.hp))
        embed.set_thumbnail(url="attachment://image.png")
        embed.add_field(name="!fight", value="\u200B", inline=False)
        embed.add_field(name="!pokemon", value="\u200B", inline=False)
        embed.add_field(name="!catch", value="\u200B", inline=False)
        embed.add_field(name="!run", value="\u200B", inline=False)
        first = pokeparty.pokemon(party.get("1"))  
        file2=discord.File("thumbnails/"+first.id+".png", filename="image2.png")
        embed.set_image(url="attachment://image2.png")
        if first.name==None:
            embed.set_footer(text=first.species+" Lv."+str(first.level)+" "+str(first.curhp)+"/"+str(first.hp))
        else:
            embed.set_footer(text=first.name+" Lv."+str(first.level)+" "+str(first.curhp)+"/"+str(first.hp))
        return [embed, file, file2]
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You aren't in a battle!")
        
    @commands.command()
    async def fight(self, ctx, *, move):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        with open("json/moves.json") as f_obj:
            moves = json.load(f_obj)
        poke1 = pokeparty.pokemon(party["1"])
        poke2 = pokeparty.pokemon(party["7"])
        battle = pokeparty.battle(poke1, poke2)
        poke2 = battle.attacks2(moves[move.lower()],"test")
        if poke2.curhp != 0:
            party["7"] = poke2.export()
            result=self.battleBox(party)
            await ctx.send(poke1.species+" used "+move.capitalize(), files=[result[1], result[2]], embed=result[0])
        else:
            del party["7"]
            await ctx.send(poke1.species+" used "+move.capitalize()+". "+poke2.species+" fainted")
        dic[str(ctx.author.id)] = party
        with open("json/parties.json", "w") as f_obj:
            json.dump(dic, f_obj, indent=4)
        
    @commands.command()
    async def pokemon(self, ctx):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        embed=discord.Embed(title="Switch to", color=discord.Color.blue())
        i=1
        while i<7:
            p = party.get(str(i))
            if p == None:
                embed.add_field(name=str(i), value="Empty", inline=False)
            if p != None:
                poke = pokeparty.pokemon(poke=p)
                if poke.name==None:
                    embed.add_field(name=str(i), value=poke.species+" Lvl: "+str(poke.level), inline=False)
                else:
                    embed.add_field(name=str(i), value=poke.name+" ("+poke.species+") Lvl: "+str(poke.level), inline=False)
            i+=1
        result = self.battleBox(party)
        await ctx.send("Type a slot number", embed=embed)
        def yes(m):
            return m.author == ctx.author
        try:
            answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out", files=[result[1], result[2]], embed=result[0])
        if int(answer.content)>6:
            await ctx.send("Invalid slot", files=[result[1], result[2]], embed=result[0])
        else:
            party1=pokeparty.party(party)
            party1.swap(1, int(answer.content))
            o=party["7"]
            party=party1.recon()
            party["7"]=o
            with open("json/parties.json") as f_obj:
                dic = json.load(f_obj)
            dic[(str(ctx.author.id))] = party
            with open("json/parties.json", "w") as f_obj:
                json.dump(dic, f_obj, indent=4)
            result = self.battleBox(party)
            outgoing = party[answer.content]
            incoming = party["1"]
            if outgoing["name"]==None:
                await ctx.send(outgoing["species"].capitalize()+" enough! Come back!")
            else: await ctx.send(outgoing["name"]+" enough! Come back!")
            if incoming["name"]==None:
                await ctx.send("Go "+incoming["species"].capitalize()+"!")
            else: await ctx.send("Go "+incoming["name"].capitalize()+"!")
            await ctx.send(files=[result[1], result[2]], embed=result[0])
    
    @commands.command()
    async def catch(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        if party.get("6")!=None:
            result = self.battleBox(party)
            await ctx.send("Can't have more than 6 pokemon", files=[result[1], result[2]], embed=result[0])
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
            add=poke.export()
            del add["catch"]
            del add["run"]
            party.add(add)
            party = party.recon()
            del party["7"]
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
            #result = self.battleBox(party)
            #await ctx.send(files=[result[1], result[2]], embed=result[0])
            return
        
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