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
            parties = json.load(f_obj)
        return parties.get(str(ctx.author.id)).get("7") != None
    
    def battleBox(self, party):
        battle = pokeparty.pokemon(party.get("7"))
        first = pokeparty.pokemon(party.get("1"))
        file=discord.File("thumbnails/"+battle.id+".png", filename="image.png")
        embed=discord.Embed(title=battle.species+" Lv."+str(battle.level), description=str(battle.curhp)+"/"+str(battle.hp))
        embed.set_thumbnail(url="attachment://image.png")
        if first.curhp!=0:
            embed.add_field(name="!fight", value="\u200B", inline=False)
        embed.add_field(name="!pokemon", value="\u200B", inline=False)
        if first.curhp!=0:
            embed.add_field(name="!catch", value="\u200B", inline=False)
        if "run2" not in party.get("7"):
            embed.add_field(name="!run", value="\u200B", inline=False)
        file2=discord.File("thumbnails/"+first.id+".png", filename="image2.png")
        embed.set_image(url="attachment://image2.png")
        if first.name==None:
            embed.set_footer(text=first.species+" Lv."+str(first.level)+" "+str(first.curhp)+"/"+str(first.hp))
        else:
            embed.set_footer(text=first.name+" Lv."+str(first.level)+" "+str(first.curhp)+"/"+str(first.hp))
        return [embed, file, file2]
    
    def is_not_dead(ctx):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        poke = pokeparty.pokemon(party.get("1"))
        return poke.curhp!=0
    
    def fainted_run(ctx):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        poke1 = pokeparty.pokemon(party.get("1"))
        poke2 = party.get("7")
        if poke1.curhp!=0:
            return 1
        elif "run2" not in poke2:
            return 1
        else:
            return 0
        
    def whited(party):
        for key in party:
            if key == "7":
                return 1
            poke = pokeparty.pokemon(party[poke])
            if poke.curhp!=0:
                return 0
            
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You can't do that right now")
        
    @commands.command()
    @commands.check(is_not_dead)
    async def fight(self, ctx):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        poke1 = pokeparty.pokemon(party["1"])
        poke2 = pokeparty.pokemon(party["7"])
        battle = pokeparty.battle(poke1, poke2)
        result=self.battleBox(party)
        with open("json/moves.json") as f_obj:
            moves = json.load(f_obj)
        move1=moves[poke1.move1.lower()]
        if poke1.move2 != None: move2=moves[poke1.move2.lower()]
        else: move2=None
        if poke1.move3 != None: move3=moves[poke1.move3.lower()]
        else: move3=None
        if poke1.move4 != None: move4=moves[poke1.move4.lower()]
        else: move3=None
        embed=discord.Embed(title="Moves", color=discord.Color.blue())
        embed.add_field(name="1: "+poke1.move1+" ("+move1["type"].capitalize()+")", value="Power: "+str(move1["power"]), inline=False)
        if poke1.move2 != None: embed.add_field(name="2: "+poke1.move2+" ("+move2["type"].capitalize()+")", value="Power: "+str(move2["power"]), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        if poke1.move3 != None: embed.add_field(name="3: "+poke1.move3+" ("+move3["type"].capitalize()+")", value="Power: "+str(move3["power"]), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        if poke1.move4 != None: embed.add_field(name="4: "+poke1.move4+" ("+move4["type"].capitalize()+")", value="Power: "+str(move4["power"]), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        await ctx.send("Type a move number", embed=embed)
        def yes(m):
            return m.author == ctx.author
        try:
            answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out", files=[result[1], result[2]], embed=result[0])
        if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
        elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
        elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
        else: omove=poke2.move1
        move5 = moves[omove.lower()]
        if int(answer.content)==1:
            move=poke1.move1
        elif int(answer.content)==2:
            if move2==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
            move=poke1.move2
        elif int(answer.content)==3:
            if move3==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
            move=poke1.move3
        elif int(answer.content)==4:
            if move4==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
            move=poke1.move4
        else:   
            return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
        val=battle.attacks2(moves[move.lower()],move5)
        poke1=battle.user
        poke2=battle.target
        party["1"]=poke1.export()
        party["7"]=poke2.export()
        result=self.battleBox(party)
        if val==0:
            if poke2.curhp == 0:
                del party["7"]
                await ctx.send(poke1.species+" used "+move.title()+". "+poke2.species+" fainted")
                win = 1
            else:
                await ctx.send(poke2.species+" used "+omove.title()+". "+poke1.species+" fainted", files=[result[1], result[2]], embed=result[0])
        else:        
            if poke2.curhp == 0:
                del party["7"]
                await ctx.send(poke2.species+" used "+omove.title()+".\n"+poke1.species+" used "+move.title()+". "+poke2.species+" fainted")
                win = 1
            if poke1.curhp == 0:
                await ctx.send(poke1.species+" used "+move.title()+".\n"+poke2.species+" used "+omove.title()+". "+poke1.species+" fainted", files=[result[1], result[2]], embed=result[0])
            else:
                if val==1:
                    await ctx.send(poke1.species+" used "+move.title()+".\n"+poke2.species+" used "+omove.title(), files=[result[1], result[2]], embed=result[0])
                else:
                    await ctx.send(poke2.species+" used "+omove.title()+".\n"+poke1.species+" used "+move.title(), files=[result[1], result[2]], embed=result[0])
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
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
        elif party.get(answer.content).get("stats").get("CurHP")==0:
            await ctx.send("Pokemon is fainted", files=[result[1], result[2]], embed=result[0])
        else:
            party1=pokeparty.party(party)
            party1.swap(1, int(answer.content))
            o=party["7"]
            party=party1.recon()
            party["7"]=o
            outgoing = party[answer.content]
            incoming = party["1"]
            poke3 = pokeparty.pokemon(outgoing)
            if poke3.curhp!=0:
                if outgoing["name"]==None:
                    await ctx.send(outgoing["species"].capitalize()+" enough! Come back!")
                else: await ctx.send(outgoing["name"]+" enough! Come back!")
            else:
                del party.get("7")["run2"]
            if incoming["name"]==None:
                await ctx.send("Go "+incoming["species"].capitalize()+"!")
            else: await ctx.send("Go "+incoming["name"].capitalize()+"!")
            if poke3.curhp!=0:                
                poke1 = pokeparty.pokemon(incoming)
                poke2 = pokeparty.pokemon(party["7"])
                battle = pokeparty.battle(poke1, poke2)
                with open("json/moves.json") as f_obj:
                    moves = json.load(f_obj)
                if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
                elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
                elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
                else: omove=poke2.move1
                battle.attacks1(move2=moves[omove.lower()])
                if poke1.curhp==0:
                    await ctx.send(poke2.species+" used "+omove.title()+". "+poke1.species+" fainted")
                else:
                    await ctx.send(poke2.species+" used "+omove.title())
                party["1"]=battle.user.export()
            result = self.battleBox(party)
            with open("json/parties.json") as f_obj:
                dic = json.load(f_obj)
            dic[(str(ctx.author.id))] = party
            with open("json/parties.json", "w") as f_obj:
                json.dump(dic, f_obj, indent=4)
            await ctx.send(files=[result[1], result[2]], embed=result[0])
    
    @commands.command()
    @commands.check(is_not_dead)
    async def catch(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        if party.get("6")!=None:
            result = self.battleBox(party)
            await ctx.send("Can't have more than 6 pokemon", files=[result[1], result[2]], embed=result[0])
            return
        poke = pokeparty.pokemon(party.get("7"))
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
            poke1 = party["1"]
            battle = pokeparty.battle(poke1,poke)
            with open("json/moves.json") as f_obj:
                moves = json.load(f_obj)
            if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
            elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
            elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
            else: omove=poke2.move1
            battle.attacks1(move2=moves[omove.lower()])
            if poke1.curhp==0:
                await ctx.send(poke2.species+" used "+omove.title()+". "+poke1.species+" fainted")
            else:
                await ctx.send(poke2.species+" used "+omove.title())
            party["1"]=battle.user.export()
            result = self.battleBox(party)
            await ctx.send(files=[result[1], result[2]], embed=result[0])
        
    @commands.command()
    @commands.check(fainted_run)
    async def run(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        poke1 = pokeparty.pokemon(party.get("1"))
        poke2 = pokeparty.pokemon(party.get("7"))
        f = poke1.speed*32/(poke2.speed/4)%256+30*party.get("7").get("run")
        g = random.randint(0,255)
        if f>g:
            del party["7"]
            parties[str(ctx.author.id)]=party
            with open("json/parties.json", "w") as f_obj:
                json.dump(parties, f_obj, indent=4)
            await ctx.send("Got away safely")
        else:
            party.get("7")["run"]+=1
            parties[str(ctx.author.id)]=party
            await ctx.send("Can't escape")
            if poke1.curhp !=0:
                battle = pokeparty.battle(poke1,poke2)
                with open("json/moves.json") as f_obj:
                    moves = json.load(f_obj)
                if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
                elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
                elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
                else: omove=poke2.move1
                battle.attacks1(move2=moves[omove.lower()])
                if poke1.curhp==0:
                    await ctx.send(poke2.species+" used "+omove.title()+". "+poke1.species+" fainted")
                else:
                    await ctx.send(poke2.species+" used "+omove.title())
                print("got here")
                party["1"]=battle.user.export()
                result = self.battleBox(party)
                await ctx.send(files=[result[1], result[2]], embed=result[0])
            else:
                party.get("7")["run2"]=1
                result = self.battleBox(party)
                await ctx.send(files=[result[1], result[2]], embed=result[0]) 
            parties[str(ctx.author.id)]=party
            with open("json/parties.json", "w") as f_obj:
                json.dump(parties, f_obj, indent=4)
    
def setup(bot):
    bot.add_cog(Fight(bot))