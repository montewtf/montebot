import discord
from discord.ext import commands
import json
import asyncio
import pokeparty
import random

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def in_fight(ctx):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return 1
        return "7" not in party
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You can't do that during a battle")
            
    @commands.command(brief="Display's your party of Pokemon", description="Display's your party of Pokemon", help="Can't be used during battle")
    @commands.check(in_fight)
    async def party(self, ctx):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return await ctx.send("You have to pick a starter first")
        embed=discord.Embed(title="Party", color=discord.Color.blue())
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
        await ctx.send(embed=embed)

    @commands.command(brief="Checks your Pokemon's summary", description="Checks your Pokemon's summary", help="slot has to be 1-6 and has to have a Pokemon in it. Can be used during battles.")
    async def summary(self, ctx, slot):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return await ctx.send("You have to pick a starter first")
        if int(slot)>6 or party.get(str(slot))==None:
            await ctx.send("Invalid slot")
            return
        p=party.get(str(slot))
        poke=pokeparty.pokemon(poke=p)
        file=discord.File("thumbnails/"+poke.id+".png", filename="image.png")
        embed=discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url="attachment://image.png")
        if poke.name==None:
            embed.add_field(name="Pokemon", value=poke.species, inline=True)
        else:
            embed.add_field(name="Pokemon", value=poke.name+" ("+poke.species+")", inline=True)
        embed.add_field(name="Level", value=poke.level, inline=True)
        if len(poke.types)==2:
            embed.add_field(name="Types", value=poke.types[0]+", "+poke.types[1], inline=False)
        else:
            embed.add_field(name="Type", value=poke.types[0], inline=False)
        
        embed.add_field(name="HP", value=str(poke.curhp)+"/"+str(poke.hp), inline=False)
        embed.add_field(name="Attack", value=poke.attack, inline=True)
        embed.add_field(name="Defense", value=poke.defense, inline=True)
        embed.add_field(name="Special", value=poke.special, inline=True)
        embed.add_field(name="Speed", value=poke.speed, inline=True)
        with open("json/moves.json") as f_obj:
            moves = json.load(f_obj)
        move1=moves[poke.move1.lower()]
        if poke.move2 != None: move2=moves[poke.move2.lower()]
        if poke.move3 != None: move3=moves[poke.move3.lower()]
        if poke.move4 != None: move4=moves[poke.move4.lower()]
        embed2=discord.Embed(title="Moves", color=discord.Color.blue())
        embed2.add_field(name=poke.move1+" ("+move1["type"].capitalize()+")", value="Power: "+str(move1["power"]), inline=False)
        if poke.move2 != None: embed2.add_field(name=poke.move2+" ("+move2["type"].capitalize()+")", value="Power: "+str(move2["power"]), inline=False)
        else: embed2.add_field(name="Empty", value="\u200B", inline=False)
        if poke.move3 != None: embed2.add_field(name=poke.move3+" ("+move3["type"].capitalize()+")", value="Power: "+str(move3["power"]), inline=False)
        else: embed2.add_field(name="Empty", value="\u200B", inline=False)
        if poke.move4 != None: embed2.add_field(name=poke.move4+" ("+move4["type"].capitalize()+")", value="Power: "+str(move4["power"]), inline=False)
        else: embed2.add_field(name="Empty", value="\u200B", inline=False)
        await ctx.send(file=file, embed=embed)
        await ctx.send(embed=embed2)
    
    def are_u_monte(ctx):
        return ctx.author.id == 125782351065251840
    
    @commands.command(hidden=True)
    @commands.check(are_u_monte)
    async def add(self, ctx, species, level, name=None):
        with open("json/pokedex.json") as f_obj:
            dex = json.load(f_obj)
        i=0
        while i<151:
            poke = dex[i]
            if species.capitalize() == poke["name"]:
             break
            i+=1
        new = pokeparty.pokemon(species=poke, level=level, name=name)
        poke = new.export()
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return await ctx.send("You have to pick a starter first")
        currentp = pokeparty.party(party)
        add=currentp.add(poke)
        if not add:
            await ctx.send("Your party is full")
            return
        party = currentp.recon()
        await ctx.send("Pokemon added to slot: "+str(add))     
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party, f_obj, indent=4)

    @commands.command(brief="Releases Pokemon", description="Releases Pokemon", help="Slot has to be 1-6 and have a pokemon in it. Gives you a chance to confirm before it releases. Can't be used in battle")
    @commands.check(in_fight)
    async def release(self, ctx, slot):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return await ctx.send("You have to pick a starter first")
        currentp = pokeparty.party(party)
        if currentp.remove(int(slot)):
            await ctx.send("Invalid slot")
            return
        await ctx.send("Are you sure you want to delete the pokemon in slot "+slot+"? (y/n)")
        def yes(m):
            return m.author == ctx.author
        try:
            answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out")
        if answer.content.lower() == "y" or answer.content.lower() == "yes":
            await ctx.send("Pokemon released")
            party = currentp.recon()
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party, f_obj, indent=4)
        elif answer.content.lower() == "n" or answer.content.lower() == "no":
            await ctx.send("Release cancelled")
        else:
            await ctx.send("Invalid answer")
        
    @commands.command(brief="Swaps Pokemon", description="Swaps Pokemon", help="Slot1 and slot2 has to be 1-6 and have pokemon in them. Slot1 and slot2 can be in any order. Can't be used in battle")
    @commands.check(in_fight)
    async def swap(self, ctx, slot1, slot2="1"):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return await ctx.send("You have to pick a starter first")
        currentp = pokeparty.party(party)
        if currentp.swap(int(slot1), int(slot2)):
            await ctx.send("Invalid slots")
            return
        party = currentp.recon()
        await ctx.send("Pokemon "+slot1+" & "+slot2+" have been swapped")
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party, f_obj, indent=4)

    @commands.command(brief="Picks a starter", description="Picks a starter", help="Starter has to be one of the kanto starters. Name is optional nickname. Can't be used with pokemon in your party")
    async def starter(self, ctx, starter, name=None):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                pass
            return await ctx.send("You have already picked a starter")
        except FileNotFoundError:
            with open("json/pokedex.json") as f_obj:
                dex = json.load(f_obj)
            if starter.lower() in ("squirtle","charmander","bulbasaur","gengar"):
                for i in (0,3,6,93):
                    poke = dex[i]
                    if starter.capitalize() == poke["name"]:
                        break
                new = pokeparty.pokemon(species=poke, level=5, name=name)
                poke = new.export()
                del poke["catch"]
                del poke["run"]
                del poke["xpyield"]
                party = {"1":poke,"2":None,"3":None,"4":None,"5":None,"6":None,}
                with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                    json.dump(party, f_obj, indent=4)
                await ctx.send("You have obtained "+str(starter).capitalize()+"!")
            else:
                await ctx.send("Invalid starter")
    @commands.command(brief="Heals Pokemon", description="Heals Pokemon", help="Can't be used in battle")
    @commands.check(in_fight)
    async def heal(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        for key in party:
            if party[key]!=None:
                poke = party[key]
                stats = poke["stats"]
                poke["status"] = None
                stats["CurHP"] = stats["HP"]
                poke["stats"] = stats
                party[key] = poke
        await ctx.send("We hope to see you again")
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party, f_obj, indent=4)
            
    @commands.command(brief="Generates a wild pokemon battle", description="Generates a wild pokemon battle", help="Wild pokemon can be any of 151 and a random level 1-100")
    async def wild(self, ctx):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
        except FileNotFoundError:
            return await ctx.send("You have to pick a starter first")
        checker = False
        if "7" not in party:
            checker = True
            with open("json/pokedex.json") as f_obj:
                dex = json.load(f_obj)
            
            poke=dex[random.randint(0, 150)]
            '''
            i=0
            while i<151:
                poke = dex[i]
                if "Electrode" == poke["name"]:
                    break
                i+=1
            '''
            level=random.randint(2,10)
            battle = pokeparty.pokemon(species=poke, level=level)
            wild = battle.export()
            party["7"] = wild
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party, f_obj, indent=4)
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        fight=self.bot.get_cog("Fight")
        result=fight.battleBox(party)
        if checker:
            await ctx.send("Wild "+battle.species+" appeared!", files=[result[1], result[2]], embed=result[0])
        else:
            await ctx.send("Already in battle", files=[result[1], result[2]], embed=result[0])
        
def setup(bot):
    bot.add_cog(Pokemon(bot))