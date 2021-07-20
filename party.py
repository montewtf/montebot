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
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
            if isinstance(error, commands.errors.CheckFailure):
                await ctx.send("You can't do that right now")
            else: raise error
        except FileNotFoundError:
            await ctx.send("You have to pick a starter first")
            
    @commands.command(brief="Display's your party of Pokemon", description="Display's your party of Pokemon", help="Can't be used during battle")
    async def party(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        embed=discord.Embed(title="Party", color=discord.Color.blue())
        i=1
        while i<7:
            p = party.get(i)
            if p == None:
                embed.add_field(name=str(i), value="Empty", inline=False)
            if p != None:
                if p.name==None:
                    embed.add_field(name=str(i), value=p.species+" Lvl: "+str(p.level), inline=False)
                else:
                    embed.add_field(name=str(i), value=p.name+" ("+p.species+") Lvl: "+str(p.level), inline=False)
            i+=1
        await ctx.send(embed=embed)
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party.export(), f_obj, indent=4)

    @commands.command(brief="Checks your Pokemon's summary", description="Checks your Pokemon's summary", help="slot has to be 1-6 and has to have a Pokemon in it. Can be used during battles.")
    async def summary(self, ctx, slot:int):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        if slot>6 or party.get(slot)==None:
            await ctx.send("Invalid slot")
            return
        poke=party.get(slot)
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
        embed2=discord.Embed(title="Moves", color=discord.Color.blue())
        embed2.add_field(name=poke.move1.name.title()+" ("+poke.move1.type.capitalize()+")", value="Power: "+str(poke.move1.power)+" PP: "+str(poke.move1.curpp)+"/"+str(poke.move1.maxpp), inline=False)
        if poke.move2 != None: embed2.add_field(name=poke.move2.name.title()+" ("+poke.move2.type.capitalize()+")", value="Power: "+str(poke.move2.power)+" PP: "+str(poke.move2.curpp)+"/"+str(poke.move2.maxpp), inline=False)
        else: embed2.add_field(name="Empty", value="\u200B", inline=False)
        if poke.move3 != None: embed2.add_field(name=poke.move3.name.title()+" ("+poke.move3.type.capitalize()+")", value="Power: "+str(poke.move3.power)+" PP: "+str(poke.move3.curpp)+"/"+str(poke.move3.maxpp), inline=False)
        else: embed2.add_field(name="Empty", value="\u200B", inline=False)
        if poke.move4 != None: embed2.add_field(name=poke.move4.name.title()+" ("+poke.move4.type.capitalize()+")", value="Power: "+str(poke.move4.power)+" PP: "+str(poke.move4.curpp)+"/"+str(poke.move4.maxpp), inline=False)
        else: embed2.add_field(name="Empty", value="\u200B", inline=False)
        await ctx.send(file=file, embed=embed)
        await ctx.send(embed=embed2)
    
    @commands.command(brief="Releases Pokemon", description="Releases Pokemon", help="Slot has to be 1-6 and have a pokemon in it. Gives you a chance to confirm before it releases. Can't be used in battle")
    @commands.check(in_fight)
    async def release(self, ctx, slot):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        if int(slot)>6:
            return await ctx.send("Invalid slot")
        party.remove(int(slot))
        await ctx.send("Are you sure you want to delete the pokemon in slot "+slot+"? (y/n)")
        def yes(m):
            return m.author == ctx.author
        try:
            answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out")
        if answer.content.lower() == "y" or answer.content.lower() == "yes":
            await ctx.send("Pokemon released")
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party.export(), f_obj, indent=4)
        elif answer.content.lower() == "n" or answer.content.lower() == "no":
            await ctx.send("Release cancelled")
        else:
            await ctx.send("Invalid answer")
        
    @commands.command(brief="Swaps Pokemon", description="Swaps Pokemon", help="Slot1 and slot2 has to be 1-6 and have pokemon in them. Slot1 and slot2 can be in any order. Can't be used in battle")
    @commands.check(in_fight)
    async def swap(self, ctx, slot1, slot2="1"):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        if party.swap(int(slot1), int(slot2)):
            return await ctx.send("Invalid slots")
        else: party.reorder()
        if int(slot2)>int(slot1): await ctx.send("Pokemon "+slot1+" & "+slot2+" have been swapped")
        else: await ctx.send("Pokemon "+slot2+" & "+slot1+" have been swapped")
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party.export(), f_obj, indent=4)

    @commands.command(brief="Picks a starter", description="Picks a starter", help="Starter has to be one of the kanto starters. Name is optional nickname. Can't be used with pokemon in your party")
    async def starter(self, ctx, starter, name=None):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                pass
            return await ctx.send("You have already picked a starter")
        except FileNotFoundError:
            with open("json/pokedex.json") as f_obj:
                dex = json.load(f_obj)
            if starter.lower() in ("squirtle","charmander","bulbasaur"):
                for i in (0,3,6):
                    poke = dex[i]
                    if starter.capitalize() == poke["name"]:
                        break
                poke = pokeparty.pokemon(species=poke, level=5, name=name)
                poke.catch = None
                poke.run = None
                poke.xpyield = None
                tdata = {"order": [1,2,3,4,5,6],
                         "level": 5,
                         "box": 1}
                party = {"0":tdata, "1":poke.export(),"2":None,"3":None,"4":None,"5":None,"6":None,}
                pc = pokeparty.pc()
                with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                    json.dump(party, f_obj, indent=4)
                with open("json/pc/"+str(ctx.author.id)+".json", "w") as f_obj:
                    json.dump(pc.export(), f_obj)
                await ctx.send("You have obtained "+str(starter).capitalize()+"!")
            else:
                await ctx.send("Invalid starter")
                
    @commands.command(brief="Heals Pokemon", description="Heals Pokemon", help="Can't be used in battle")
    @commands.check(in_fight)
    async def heal(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        i=1
        while i<7:
            if party.get(i)!=None:
                poke = party.get(i)
                poke.resetMod()
                list1=[poke.move1,poke.move2,poke.move3,poke.move4]
                for move in list1:
                    if move!=None:
                        move.curpp=move.maxpp
                poke.move1,poke.move2,poke.move3,poke.move4 = list1
                poke.status = {}
                poke.curhp =  poke.hp
                party.setp(i,poke)
            i+=1
        await ctx.send("We hope to see you again")
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party.export(), f_obj, indent=4)
            
    @commands.command(brief="Generates a wild pokemon battle", description="Generates a wild pokemon battle", help="Wild pokemon can be any of 151 and a random level 1-100")
    async def wild(self, ctx, area=None):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        checker = False
        if party.p7==None:
            checker = True
            i=2
            while "fainted" in party.p1.status:
                party.swap(1,i)
                if i==7 or party.p1==None:
                    return await ctx.send("All your pokemon are fainted")
                i+=1
            with open("json/wild.json") as f_obj:
                spawns = json.load(f_obj)
            newspawns = {}
            string = ""
            embed=discord.Embed(title="Available Areas", color=discord.Color.blue())
            for key in spawns:
                if int(key) <= party.level:
                    for key2 in spawns[key]:
                        newspawns[key2] = spawns[key][key2]
                        string += key2+"\n"
                    embed.add_field(name=key, value=string, inline=False)
                    string = ""
                else: break
            if area == None:
                def yes(m):
                    return m.author == ctx.author
                await ctx.send("Select an area", embed=embed)
                try:
                    answer = await self.bot.wait_for("message", check=yes, timeout=30.0)
                except asyncio.TimeoutError:
                    return await ctx.send("Timed out")
                area = answer.content
            if area not in newspawns:
                return await ctx.send("Invalid Area")
            else:
                area = newspawns[area]
            choice = random.choices(area[0], area[1])[0]
            with open("json/pokedex.json") as f_obj:
                dex = json.load(f_obj)
            poke=dex[choice[0]-1]
            level=random.randint(choice[1],choice[2])
            party.p7 = pokeparty.pokemon(species=poke, level=level)
            party.p1.part = True
        fight=self.bot.get_cog("Fight")
        result=fight.battleBox(party)
        if checker:
            await ctx.send("Wild "+party.p7.species+" appeared!", files=[result[1], result[2]], embed=result[0])
        else:
            await ctx.send("Already in battle", files=[result[1], result[2]], embed=result[0])
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party.export(), f_obj, indent=4)
    
    @commands.command(brief="Accesses PC", description="Accesses PC", help="Brings up a popup and waits for a response for the slot. Can't be used in battle")
    @commands.check(in_fight)
    async def pc(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        with open("json/pc/"+str(ctx.author.id)+".json") as f_obj:
            pc = pokeparty.pc(json.load(f_obj))
        embed=discord.Embed(title="Monte's PC", color=discord.Color.blue())
        embed.add_field(name="1. Withdraw Pokemon", value="\u200B", inline=False)
        embed.add_field(name="2. Deposit Pokemon", value="\u200B", inline=False)
        embed.add_field(name="3. Release Pokemon", value="\u200B", inline=False)
        embed.add_field(name="4. Change box", value="\u200B", inline=False)
        def yes(m):
            return m.author == ctx.author
        await ctx.send("PC accessed (10 second timeout)", embed=embed)
        try:
            answer1 = await self.bot.wait_for("message", check=yes, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out")
        answer1 = int(answer1.content)
        if answer1 == 1: title = "Withdraw Pokemon"
        elif answer1 == 2: title = "Deposit Pokemon"
        elif answer1 == 3: title = "Release Pokemon"
        elif answer1 == 4: title = "Change box"
        else: return await ctx.send("Invalid Input")
        embed2=discord.Embed(title=title, color=discord.Color.blue())
        if answer1 == 4:
            i = 1
            while i <= 8:
                tbox = pc.get_box(i)
                embed2.add_field(name=str(i)+" - "+str(len(tbox))+"/30", value="\u200B", inline=False)
                i+=1
        elif answer1 != 2:
            tbox = pc.get_box()
            i = 0
            string = ""
            while i < len(tbox):
                p = pokeparty.pokemon(tbox[i])
                string += str(i+1)+" "+p.species+" Lvl:"+str(p.level)+"\n"
                i+=1
            embed2.add_field(name="\u200B", value=string, inline=False)
        else:
            i = 1
            while i < 7:
                p = party.get(i)
                if p == None:
                    embed2.add_field(name=str(i), value="Empty", inline=False)
                elif p != None:
                    embed2.add_field(name=str(i), value=p.species+" Lvl: "+str(p.level), inline=False)
                i+=1
        await ctx.send("Make your selection (30 second timeout)", embed=embed2)
        try:
            answer2 = await self.bot.wait_for("message", check=yes, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out")
        answer2 = int(answer2.content)
        if answer1 == 1:
            if answer2 > len(tbox) or answer2 < 1:
                return await ctx.send("Invalid Input")
            if party.p6 != None:
                return await ctx.send("Party Full")
            poke = pokeparty.pokemon(pc.withdraw(answer2))
            slot = party.add(poke)
            await ctx.send(poke.species+" withdrawn to slot "+str(slot))
        elif answer1 == 2:
            tbox = pc.get_box()
            if len(tbox) == 30:
                return await ctx.send("Box is Full")
            if party.get(answer2) == None:
                return await ctx.send("Invalid Input")
            poke = party.remove(answer2)
            pc.deposit(poke.export())
            await ctx.send(poke.species+" deposited to box "+str(pc.main))
        elif answer1 == 3:
            if answer2 > len(tbox):
                return await ctx.send("Invalid Input")
            await ctx.send("Are you sure you want to delete "+tbox[answer2-1]["species"]+"? (y/n)")
            try:
                answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
            except asyncio.TimeoutError:
                return await ctx.send("Timed out")
            if answer.content.lower() == "y" or answer.content.lower() == "yes":
                pc.release(answer2)
                await ctx.send("Pokemon released")
            elif answer.content.lower() == "n" or answer.content.lower() == "no":
                return await ctx.send("Release cancelled")
            else:
                return await ctx.send("Invalid answer")
        elif answer1 == 4:
            if answer2 > 8:
                return await ctx.send("Invalid Input")
            pc.main = answer2
            await ctx.send("Box was changed to "+str(answer2))
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party.export(), f_obj, indent=4)
        with open("json/pc/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(pc.export(), f_obj)
    
def setup(bot):
    bot.add_cog(Pokemon(bot))