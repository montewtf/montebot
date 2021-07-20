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
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = pokeparty.party(json.load(f_obj))
            return party.get(7)!=None
        except FileNotFoundError:
            return 0
    
    def battleBox(self, party):
        ustatus=party.p1.getvolstatus()
        tstatus=party.p7.getvolstatus()
        file=discord.File("thumbnails/"+party.p7.id+".png", filename="image.png")
        embed=discord.Embed(title=party.p7.species+" Lv."+str(party.p7.level), description=str(party.p7.curhp)+"/"+str(party.p7.hp)+tstatus)
        embed.set_thumbnail(url="attachment://image.png")
        if party.p1.curhp!=0:
            embed.add_field(name="!fight", value="\u200B", inline=False)
        embed.add_field(name="!pokemon", value="\u200B", inline=False)
        if party.p1.curhp!=0:
            embed.add_field(name="!catch", value="\u200B", inline=False)
        if party.p7.run2==None:
            embed.add_field(name="!run", value="\u200B", inline=False)
        file2=discord.File("thumbnails/"+party.p1.id+".png", filename="image2.png")
        embed.set_image(url="attachment://image2.png")
        if party.p1.name==None:
            embed.set_footer(text=party.p1.species+" Lv."+str(party.p1.level)+" "+str(party.p1.curhp)+"/"+str(party.p1.hp)+ustatus)
        else:
            embed.set_footer(text=party.p1.name+" Lv."+str(party.p1.level)+" "+str(party.p1.curhp)+"/"+str(party.p1.hp)+ustatus)
        return [embed, file, file2]
    
    def is_not_dead(ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        return party.p1.curhp!=0
    
    def fainted_run(ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        if party.p1.curhp!=0:
            return 1
        elif not party.p7.run2:
            return 1
        else:
            return 0
        
    def whited(self, party):
        i=1
        while i<7:
            if party.get(i)!=None:
                if party.get(i).curhp!=0:
                    return 0
            i+=1
        return 1
    
    async def turn(self, ctx, party, string):
        result=self.battleBox(party)
        win = 0
        if party.p1.curhp==0:
            party.p1.status={"fainted": None}
            result=self.battleBox(party)
            party.p1.part=None
            party.p1.resetMod()
            if self.whited(party):
                await ctx.send(string)
                await ctx.send("You blacked out")
                i=1
                while i<7:
                    if party.get(i)!=None:
                        if party.get(i).part!=None:
                            p=party.get(i)
                            p.part=None
                            party.setp(i,p)
                    i+=1
                party.unswap()
                party.p7=None
        if party.p7 !=None:
            if party.p7.curhp == 0 and not self.whited(party):
                await ctx.send(string)
                win = 1
            else:
                await ctx.send(string, files=[result[1], result[2]], embed=result[0])
        if win==1:
            i=1
            part=0
            while i<7:
                if party.get(i)!=None:
                    if party.get(i).part!=None:
                       part+=1
                i+=1
            if part == 0: part = 1
            xp = math.floor(party.p7.xpyield*party.p7.level/(7*part))
            evgain = party.p7.base
            party.p7=None
            i=1
            part=0
            levelled={}
            while i<7:
                if party.get(i)!=None:
                    tpoke = party.get(i)
                    if "toxic" in party.get(i).status:
                        del tpoke.status["toxic"]
                        tpoke.status["poison"] = None
                    for key in party.p1.status:
                        if key == "fainted": break
                        if key in ["freeze", "paralysis", "burn", "sleep", "poison"]:
                            party.p1.status = {key: party.p1.status[key]}
                            break
                    if party.get(i).part!=None:
                        tpoke.resetMod()
                        tpoke.curxp+=xp
                        curev=tpoke.getEV()
                        for key in evgain:
                            curev[key]+=evgain[key]
                        tpoke.setEV(curev)
                        await ctx.send(tpoke.species+" earned "+str(xp)+" xp")
                        result2=tpoke.levelup()
                        tpoke.part=None
                        if result2[0]:
                            result3=result2[3]
                            embed=discord.Embed(title=tpoke.species, color=discord.Color.blue())
                            embed.add_field(name="HP", value="+"+str(result3[0]), inline=False)
                            embed.add_field(name="Attack", value="+"+str(result3[1]), inline=False)
                            embed.add_field(name="Defense", value="+"+str(result3[2]), inline=False)
                            embed.add_field(name="Speed", value="+"+str(result3[3]), inline=False)
                            embed.add_field(name="Special", value="+"+str(result3[4]), inline=False)
                            await ctx.send(tpoke.species+" grew to level "+str(tpoke.level), embed=embed)
                            levelled[str(i)]=tpoke
                            if result2[1]>0:
                                already = False
                                for element in [tpoke.move1,tpoke.move2,tpoke.move3,tpoke.move4]:
                                    if element != None:
                                        if result2[2]==element.name.title():
                                            already = True
                                if result2[1]==1 and not already:
                                    await ctx.send(tpoke.species+" learned "+result2[2].title())
                                if result2[1]==2 and not already:
                                    embed=discord.Embed(title="Moves", color=discord.Color.blue())
                                    embed.add_field(name="1", value=tpoke.move1.name.title(), inline=False)
                                    embed.add_field(name="2", value=tpoke.move2.name.title(), inline=False)
                                    embed.add_field(name="3", value=tpoke.move3.name.title(), inline=False)
                                    embed.add_field(name="4", value=tpoke.move4.name.title(), inline=False)
                                    embed.add_field(name="5", value=result2[2], inline=False)
                                    await ctx.send(tpoke.species+" is trying to learn "+result2[2]+", but it already knows 4 moves. Which move should be replaced?", embed=embed)
                                    def yes(m):
                                        return m.author == ctx.author
                                    answer2 = await self.bot.wait_for("message", check=yes)
                                    if answer2.content in ["1","2","3","4"]:
                                        answer2.content=int(answer2.content)
                                        await ctx.send(tpoke.species+" forgot "+tpoke.getMove(answer2.content).name.title())
                                        await ctx.send(tpoke.species+" learned "+result2[2])
                                        tpoke.addMove(result2[2],answer2.content)
                                    else:
                                        await ctx.send(tpoke.species+" did not learn "+result2[2])
                    party.setp(i,tpoke)
                i+=1
            with open("json/pokedex.json") as f_obj:
                pokedex = json.load(f_obj)
            for key in levelled:
                epoke = levelled[key]
                dex = pokedex[int(epoke.id)-1]
                if dex.get("evolvesat")!=None and int(dex.get("evolvesat"))<=epoke.level:
                    answer=None
                    await ctx.send(epoke.species+" is trying to evolve. (Type anything in the next 15 seconds to cancel)")
                    try:
                        answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
                    except asyncio.TimeoutError:
                        oldpoke=epoke.species
                        epoke.evolve(pokedex[int(dex["evolvesto"])-1])
                        await ctx.send(oldpoke+" evolved into "+epoke.species)
                    if answer!=None:
                        await ctx.send(epoke.species+" stopped evolving")
                    party.set(int(key),epoke)
            party.unswap()
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party.export(), f_obj, indent=4)
            
    async def cog_command_error(self, ctx, error):
        try:
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party = json.load(f_obj)
            if isinstance(error, commands.errors.CheckFailure):
                await ctx.send("You can't do that right now")
            else: raise error
        except FileNotFoundError:
            await ctx.send("You have to pick a starter first")
        
    @commands.command()
    @commands.check(is_not_dead)
    async def fight(self, ctx, slot=0):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        result=self.battleBox(party)
        embed=discord.Embed(title="Moves", color=discord.Color.blue())
        embed.add_field(name=party.p1.move1.name.title()+" ("+party.p1.move1.type.capitalize()+")", value="Power: "+str(party.p1.move1.power)+" PP: "+str(party.p1.move1.curpp)+"/"+str(party.p1.move1.maxpp), inline=False)
        if party.p1.move2 != None: embed.add_field(name=party.p1.move2.name.title()+" ("+party.p1.move2.type.capitalize()+")", value="Power: "+str(party.p1.move2.power)+" PP: "+str(party.p1.move2.curpp)+"/"+str(party.p1.move2.maxpp), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        if party.p1.move3 != None: embed.add_field(name=party.p1.move3.name.title()+" ("+party.p1.move3.type.capitalize()+")", value="Power: "+str(party.p1.move3.power)+" PP: "+str(party.p1.move3.curpp)+"/"+str(party.p1.move3.maxpp), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        if party.p1.move4 != None: embed.add_field(name=party.p1.move4.name.title()+" ("+party.p1.move4.type.capitalize()+")", value="Power: "+str(party.p1.move4.power)+" PP: "+str(party.p1.move4.curpp)+"/"+str(party.p1.move4.maxpp), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        for move in [party.p1.move1,party.p1.move2,party.p1.move3,party.p1.move4]:
            if move!=None:
                if move.curpp>0:
                    struggle=False
                    break
                else:
                    struggle=True
        if struggle:
            movenum=0
        elif int(slot) in [1,2,3,4]:
            if int(slot)==1: movenum=1
            elif int(slot)==2: movenum=2
            elif int(slot)==3: movenum=3
            elif int(slot)==4: movenum=4  
        else:
            def yes(m):
                return m.author == ctx.author
            await ctx.send("Type a move number", embed=embed)
            try:
                answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
            except asyncio.TimeoutError:
                return await ctx.send("Timed out", files=[result[1], result[2]], embed=result[0])
            try:
                movenum=int(answer.content)
            except ValueError:
                if answer.content.startswith("!"): return
                return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
            if movenum<=4 and movenum>0:
                if party.p1.getMove(movenum)==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
                elif party.p1.getMove(movenum).curpp==0: return await ctx.send("That move has no pp", files=[result[1], result[2]], embed=result[0])
            else:   
                return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
        if party.p7.move4 != None:omove=random.randint(1,4)
        elif party.p7.move3 != None:omove=random.randint(1,3)
        elif party.p7.move2 != None:omove=random.randint(1,2)
        else: omove=1
        party.p7.run=1
        battle = pokeparty.battle(party.p1, party.p7)
        string=battle.turn(movenum,omove)
        party.p1, party.p7 = battle.user, battle.target
        await self.turn(ctx, party, string)
        
    @commands.command()
    async def pokemon(self, ctx, slot=0):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        embed=discord.Embed(title="Switch to", color=discord.Color.blue())
        i=1
        while i<7:
            p=party.get(i)
            if p == None:
                embed.add_field(name=str(i), value="Empty", inline=False)
            if p != None:
                if p.name==None:
                    embed.add_field(name=str(i), value=p.species+" Lvl: "+str(p.level), inline=False)
                else:
                    embed.add_field(name=str(i), value=p.name+" ("+p.species+") Lvl: "+str(p.level), inline=False)
            i+=1
        result = self.battleBox(party)
        if int(slot) in [1,2,3,4]:
            if int(slot)==1: pokenum=1
            elif int(slot)==2: pokenum=2
            elif int(slot)==3: pokenum=3
            elif int(slot)==4: pokenum=4  
        else:
            def yes(m):
                return m.author == ctx.author
            await ctx.send("Type a slot number", embed=embed)
            try:
                answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
            except asyncio.TimeoutError:
                return await ctx.send("Timed out", files=[result[1], result[2]], embed=result[0])
            try:
                pokenum=int(answer.content)
            except ValueError:
                if answer.content.startswith("!"): return
                return await ctx.send("Invalid slot", files=[result[1], result[2]], embed=result[0])
        if pokenum>6 or party.get(pokenum)==None:
            await ctx.send("Invalid slot", files=[result[1], result[2]], embed=result[0])
        elif party.get(pokenum).curhp==0:
            await ctx.send("Pokemon is fainted", files=[result[1], result[2]], embed=result[0])
        else:
            party.p1.resetMod()
            if "toxic" in party.p1.status:
                del party.p1.status["toxic"]
                party.p1.status["poison"] = None
            for key in party.p1.status:
                if key == "fainted": break
                if key in ["freeze", "paralysis", "burn", "sleep", "poison"]:
                    party.p1.status = {key: party.p1.status[key]}
                    break
            party.swap(pokenum)
            outgoing = party.get(pokenum)
            party.p1.part=True
            if outgoing.curhp!=0:
                if outgoing.name==None:
                    await ctx.send(outgoing.species.capitalize()+" enough! Come back!")
                else: await ctx.send(outgoing.name+" enough! Come back!")
            else:
                party.p7.run2=None
            if party.p1.name==None:
                await ctx.send("Go "+party.p1.species.capitalize()+"!")
            else: await ctx.send("Go "+party.p1.name.capitalize()+"!")
            if outgoing.curhp!=0:
                if party.p7.move4 != None:omove=random.randint(1,4)
                elif party.p7.move3 != None:omove=random.randint(1,3)
                elif party.p7.move2 != None:omove=random.randint(1,2)
                else: omove=1
                battle = pokeparty.battle(party.p1, party.p7)
                string=battle.turn(move2=omove)
                party.p1, party.p7 = battle.user, battle.target
                await self.turn(ctx, party, string)
            else:
                result=self.battleBox(party)
                await ctx.send(files=[result[1], result[2]], embed=result[0])
                with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                    json.dump(party.export(), f_obj, indent=4)
    
    @commands.command()
    @commands.check(is_not_dead)
    async def catch(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        with open("json/pc/"+str(ctx.author.id)+".json") as f_obj:
            pc = pokeparty.pc(json.load(f_obj))
        if party.p6!=None and len(pc.get_box()) > 30:
            result = self.battleBox(party)
            return await ctx.send("Party and current box full", files=[result[1], result[2]], embed=result[0])
        r1 = random.randint(0,255)
        if party.p7.status in ["sleep", "freeze"]:
            s=25
        elif party.p7.status in ["poison", "burn", "paralysis"]:
            s=12
        else: s=0
        r = r1-s
        f = math.floor(party.p7.hp*255/12)
        h = math.floor(party.p7.curhp/4)
        if h==0:h=1
        f = math.floor(f/h)
        if r < 0:
            caught = True
        elif party.p7.catch < r:
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
            await ctx.send("You caught a "+party.p7.species+"!")
            party.p7.catch=None
            party.p7.run=None
            party.p7.run2=None
            party.p7.xpyield=None
            party.unswap()
            if party.p6 == None:
                party.add(party.p7)
            else:
                pc.deposit(party.p7.export())
                await ctx.send("Your party was full. "+party.p7.species+" was added to Box "+str(pc.main))
            party.p7=None
            i=1
            while i<7:
                if party.get(i)!=None:
                    if party.get(i).part!=None:
                        p=party.get(i)
                        p.resetMod()
                        p.part=None
                        party.setp(i,p)
                i+=1
            with open("json/pc/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(pc.export(), f_obj)
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party.export(), f_obj, indent=4)
        else:
            w = math.floor(100*party.p7.catch/255)
            w = math.floor(w*f/255)
            if party.p7.status in ["sleep", "freeze"]:
                w+=10
            elif party.p7.status in ["poison", "burn", "paralysis"]:
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
            if party.p7.move4 != None:omove=random.randint(1,4)
            elif party.p7.move3 != None:omove=random.randint(1,3)
            elif party.p7.move2 != None:omove=random.randint(1,2)
            else: omove=1
            battle = pokeparty.battle(party.p1, party.p7)
            string=battle.turn(move2=omove)
            party.p1, party.p7 = battle.user, battle.target
            await self.turn(ctx, party, string)
        
    @commands.command()
    @commands.check(fainted_run)
    async def run(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = pokeparty.party(json.load(f_obj))
        f = party.p1.speed*32/(party.p7.speed/4)%256+30*party.p7.run
        g = random.randint(0,255)
        if f>g:
            i=1
            while i<7:
                if party.get(i)!=None:
                    if party.get(i).part!=None:
                        p=party.get(i)
                        p.resetMod()
                        p.part=None
                        party.setp(i,p)
                i+=1
            party.p7=None
            party.unswap()
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party.export(), f_obj, indent=4)
            await ctx.send("Got away safely")
        else:
            party.p7.run+=1
            await ctx.send("Can't escape")
            if party.p1.curhp !=0:
                if party.p7.move4 != None:omove=random.randint(1,4)
                elif party.p7.move3 != None:omove=random.randint(1,3)
                elif party.p7.move2 != None:omove=random.randint(1,2)
                else: omove=1
                battle = pokeparty.battle(party.p1, party.p7)
                string=battle.turn(move2=omove)
                party.p1, party.p7 = battle.user, battle.target
                await self.turn(ctx, party, string)
            else:
                party.p7.run2=True
                result=self.battleBox(party)
                await ctx.send(files=[result[1], result[2]], embed=result[0])
                with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                    json.dump(party.export(), f_obj, indent=4)

def setup(bot):
    bot.add_cog(Fight(bot))