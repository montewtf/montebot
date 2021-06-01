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
                party = json.load(f_obj)
            return party.get("7") != None
        except FileNotFoundError:
            return 0
    
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
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        poke = pokeparty.pokemon(party.get("1"))
        return poke.curhp!=0
    
    def fainted_run(ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        poke1 = pokeparty.pokemon(party.get("1"))
        poke2 = party.get("7")
        if poke1.curhp!=0:
            return 1
        elif "run2" not in poke2:
            return 1
        else:
            return 0
        
    def whited(self, party):
        for key in party:
            if key == "7":
                return 1
            if party[key]!=None:
                poke = pokeparty.pokemon(party[key])
                if poke.curhp!=0:
                    return 0
            
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
    async def fight(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        poke1 = pokeparty.pokemon(party["1"])
        poke2 = pokeparty.pokemon(party["7"])
        battle = pokeparty.battle(poke1, poke2)
        result=self.battleBox(party)
        embed=discord.Embed(title="Moves", color=discord.Color.blue())
        embed.add_field(name=poke1.move1.name.title()+" ("+poke1.move1.type.capitalize()+")", value="Power: "+str(poke1.move1.power)+" PP: "+str(poke1.move1.curpp)+"/"+str(poke1.move1.maxpp), inline=False)
        if poke1.move2 != None: embed.add_field(name=poke1.move2.name.title()+" ("+poke1.move2.type.capitalize()+")", value="Power: "+str(poke1.move2.power)+" PP: "+str(poke1.move2.curpp)+"/"+str(poke1.move2.maxpp), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        if poke1.move3 != None: embed.add_field(name=poke1.move3.name.title()+" ("+poke1.move3.type.capitalize()+")", value="Power: "+str(poke1.move3.power)+" PP: "+str(poke1.move3.curpp)+"/"+str(poke1.move3.maxpp), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        if poke1.move4 != None: embed.add_field(name=poke1.move4.name.title()+" ("+poke1.move4.type.capitalize()+")", value="Power: "+str(poke1.move4.power)+" PP: "+str(poke1.move4.curpp)+"/"+str(poke1.move4.maxpp), inline=False)
        else: embed.add_field(name="Empty", value="\u200B", inline=False)
        for move in [poke1.move1,poke1.move2,poke1.move3,poke1.move4]:
            if move!=None:
                if move.curpp>0:
                    bool1=False
                    break
                else:
                    bool1=True
        if bool1:
            move=pokeparty.move("struggle")
        else:
            await ctx.send("Type a move number", embed=embed)
            def yes(m):
                return m.author == ctx.author
            try:
                answer = await self.bot.wait_for("message", check=yes, timeout=10.0)
            except asyncio.TimeoutError:
                return await ctx.send("Timed out", files=[result[1], result[2]], embed=result[0])
            if int(answer.content)==1:
                if poke1.move1.curpp==0: return await ctx.send("That move has no pp", files=[result[1], result[2]], embed=result[0])
                move=poke1.move1
                poke1.move1.curpp-=1
            elif int(answer.content)==2:
                if poke1.move2==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
                elif poke1.move2.curpp==0: return await ctx.send("That move has no pp", files=[result[1], result[2]], embed=result[0])
                move=poke1.move2
                poke1.move2.curpp-=1
            elif int(answer.content)==3:
                if poke1.move3==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
                elif poke1.move3.curpp==0: return await ctx.send("That move has no pp", files=[result[1], result[2]], embed=result[0])
                move=poke1.move
                poke1.move3.curpp-=1
            elif int(answer.content)==4:
                if poke1.move4==None: return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
                elif poke1.move4.curpp==0: return await ctx.send("That move has no pp", files=[result[1], result[2]], embed=result[0])
                move=poke1.move4
                poke1.move4.curpp-=1
            else:   
                return await ctx.send("Invalid move", files=[result[1], result[2]], embed=result[0])
        if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
        elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
        elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
        else: omove=poke2.move1
        rlist=battle.attacks2(move,omove)
        val=rlist[0]
        t1=rlist[1]
        t2=1
        if len(rlist)>2:t2=rlist[2]
        if t1==0:effective1="It's not effective. "
        elif t1<1:effective1="It's not very effective. "
        elif t1>1:effective1="It's super effective. "
        else:effective1=""
        if t2==0:effective2="It's not effective. "
        elif t2<1:effective2="It's not very effective. "
        elif t2>1:effective2="It's super effective. "
        else:effective2=""
        poke1=battle.user
        poke2=battle.target
        if poke1.curhp==0:
            poke1.status="fainted"
            poke1.part=None
        party["1"]=poke1.export()
        party["7"]=poke2.export()
        result=self.battleBox(party)
        win = 0
        if val==0:
            if poke2.curhp == 0:
                del party["7"]
                await ctx.send(poke1.species+" used "+move.name.title()+". "+effective1+poke2.species+" fainted")
                win = 1
            else:
                if self.whited(party):
                    await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+poke1.species+" fainted")
                    await ctx.send("You blacked out")
                    del party["7"]
                else:
                    await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+poke1.species+" fainted", files=[result[1], result[2]], embed=result[0])
        else:
            if poke2.curhp == 0:
                del party["7"]
                await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+"\n"+poke1.species+" used "+move.name.title()+". "+effective2+poke2.species+" fainted")
                win = 1
            elif poke1.curhp == 0:
                if self.whited(party):
                    await ctx.send(poke1.species+" used "+move.name.title()+". "+effective1+"\n"+poke2.species+" used "+omove.name.title()+". "+effective1+poke1.species+" fainted")
                    await ctx.send("You blacked out")
                    i=1
                    while i<7:
                        if party[str(i)] != None:
                            del party[str(i)]["participated"]
                        i+=1
                    del party["7"]
                else:
                    await ctx.send(poke1.species+" used "+move.name.title()+". "+effective1+"\n"+poke2.species+" used "+omove.name.title()+". "+effective2+poke1.species+" fainted", files=[result[1], result[2]], embed=result[0])
            else:
                if val==1:
                    await ctx.send(poke1.species+" used "+move.name.title()+". "+effective1+"\n"+poke2.species+" used "+omove.name.title()+". "+effective2, files=[result[1], result[2]], embed=result[0])
                else:
                    await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+"\n"+poke1.species+" used "+move.name.title()+". "+effective2, files=[result[1], result[2]], embed=result[0])
        if win==1:
            i=1
            part=0
            while i<7:
                if party[str(i)]!=None:
                    if "participated" in party[str(i)]:
                        part+=1
                i+=1
            xp = math.floor(poke2.xpyield*poke2.level/(7*part))
            i=1
            part=0
            while i<7:
                if party[str(i)]!=None:
                    if "participated" in party[str(i)]:
                        tpoke = pokeparty.pokemon(party[str(i)])
                        tpoke.curxp+=xp
                        await ctx.send(tpoke.species+" earned "+str(xp)+" xp")
                        result2=tpoke.levelup()
                        if result2[0]:
                            await ctx.send(tpoke.species+" grew to level "+str(tpoke.level))
                            if result2[1]>0:
                                if result2[1]==1:
                                    await ctx.send(tpoke.species+" learned "+result2[2].title())
                                if result2[1]==2:
                                    embed=discord.Embed(title="Moves", color=discord.Color.blue())
                                    embed.add_field(name="1", value=tpoke.move1.name.title(), inline=False)
                                    embed.add_field(name="2", value=tpoke.move2.name.title(), inline=False)
                                    embed.add_field(name="3", value=tpoke.move3.name.title(), inline=False)
                                    embed.add_field(name="4", value=tpoke.move4.name.title(), inline=False)
                                    embed.add_field(name="5", value=result2[2], inline=False)
                                    await ctx.send(tpoke.species+" is trying to learn "+result2[2]+", but it already knows 4 moves. Which move should be replaced?", embed=embed)
                                    answer2 = await self.bot.wait_for("message", check=yes)
                                    if answer2.content == "1":
                                        await ctx.send(tpoke.species+" forgot "+tpoke.move1.name.title())
                                        await ctx.send(tpoke.species+" learned "+result2[2])
                                        tpoke.addMove(result2[2],1)
                                    elif answer2.content == "2":
                                        await ctx.send(tpoke.species+" forgot "+tpoke.move2.name.title())
                                        await ctx.send(tpoke.species+" learned "+result2[2])
                                        tpoke.addMove(result2[2],2)
                                    elif answer2.content == "3":
                                        await ctx.send(tpoke.species+" forgot "+tpoke.move3.name.title())
                                        await ctx.send(tpoke.species+" learned "+result2[2])
                                        tpoke.addMove(result2[2],3)
                                    elif answer2.content == "4":
                                        await ctx.send(tpoke.species+" forgot "+tpoke.move4.name.title())
                                        await ctx.send(tpoke.species+" learned "+result2[2])
                                        tpoke.addMove(result2[2],4)
                                    else:
                                        await ctx.send(tpoke.species+" did not learn "+result2[2])
                                    
                        party[str(i)] = tpoke.export()
                i+=1
        with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
            json.dump(party, f_obj, indent=4)
        
    @commands.command()
    async def pokemon(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
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
            party["1"]["participated"]=True
            incoming = party["1"]
            poke3 = pokeparty.pokemon(outgoing)
            if poke3.curhp!=0:
                if outgoing["name"]==None:
                    await ctx.send(outgoing["species"].capitalize()+" enough! Come back!")
                else: await ctx.send(outgoing["name"]+" enough! Come back!")
            else:
                if "run2" in party["7"]:
                    del party.get("7")["run2"]
            if incoming["name"]==None:
                await ctx.send("Go "+incoming["species"].capitalize()+"!")
            else: await ctx.send("Go "+incoming["name"].capitalize()+"!")
            if poke3.curhp!=0:                
                poke1 = pokeparty.pokemon(incoming)
                poke2 = pokeparty.pokemon(party["7"])
                battle = pokeparty.battle(poke1, poke2)
                if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
                elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
                elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
                else: omove=poke2.move1
                battle.attacks1(move2=omove.lower)
                if poke1.curhp==0:
                    battle.user.status="fainted"
                    if self.whited(party):
                        await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+poke1.species+" fainted")
                        await ctx.send("You blacked out")
                        i=1
                        while i<7:
                            if party[str(i)] != None:
                                del party[str(i)]["participated"]
                            i+=1
                        del party["7"]
                    else:
                        await ctx.send(poke2.species+" used "+omove.name.title()+". "+poke1.species+" fainted")
                else:
                    await ctx.send(poke2.species+" used "+omove.name.title())
                party["1"]=battle.user.export()
            result = self.battleBox(party)
            with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
                party2 = json.load(f_obj)
            party2 = party
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party2, f_obj, indent=4)
            if not self.whited(party):
                await ctx.send(files=[result[1], result[2]], embed=result[0])
    
    @commands.command()
    @commands.check(is_not_dead)
    async def catch(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        if party.get("6")!=None:
            result = self.battleBox(party)
            await ctx.send("Can't have more than 6 pokemon", files=[result[1], result[2]], embed=result[0])
            return
        poke2 = pokeparty.pokemon(party.get("7"))
        r1 = random.randint(0,255)
        if poke2.status in ["sleep", "freeze"]:
            s=25
        elif poke2.status in ["poison", "burn", "paralysis"]:
            s=12
        else: s=0
        r = r1-s
        f = math.floor(poke2.hp*255/12)
        h = math.floor(poke2.curhp/4)
        if h==0:h=1
        f = math.floor(f/h)
        if r < 0:
            caught = True
        elif poke2.catch < r:
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
            await ctx.send("You caught a "+poke2.species+"!")
            party = pokeparty.party(party)
            add=poke2.export()
            del add["catch"]
            del add["run"]
            del add["xpyield"]
            party.add(add)
            party = party.recon()
            del party["7"]
            i=1
            while i<7:
                if party[str(i)] != None:
                    del party[str(i)]["participated"]
                i+=1
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party, f_obj, indent=4)
        else:
            w = math.floor(100*poke2.catch/255)
            w = math.floor(w*f/255)
            if poke2.status in ["sleep", "freeze"]:
                w+=10
            elif poke2.status in ["poison", "burn", "paralysis"]:
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
            poke1 = pokeparty.pokemon(party["1"])
            battle = pokeparty.battle(poke1,poke2)
            if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
            elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
            elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
            else: omove=poke2.move1
            battle.attacks1(move2=omove)
            if poke1.curhp==0:
                battle.user.status="fainted"
                if self.whited(party):
                    await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+poke1.species+" fainted")
                    await ctx.send("You blacked out")
                    i=1
                    while i<7:
                        if party[str(i)] != None:
                            del party[str(i)]["participated"]
                        i+=1
                    del party["7"]
                else:
                    await ctx.send(poke2.species+" used "+omove.name.title()+". "+poke1.species+" fainted")
            else:
                await ctx.send(poke2.species+" used "+omove.name.title())
            party["1"]=battle.user.export()
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party, f_obj, indent=4)
            result = self.battleBox(party)
            await ctx.send(files=[result[1], result[2]], embed=result[0])
        
    @commands.command()
    @commands.check(fainted_run)
    async def run(self, ctx):
        with open("json/parties/"+str(ctx.author.id)+".json") as f_obj:
            party = json.load(f_obj)
        poke1 = pokeparty.pokemon(party.get("1"))
        poke2 = pokeparty.pokemon(party.get("7"))
        f = poke1.speed*32/(poke2.speed/4)%256+30*party.get("7").get("run")
        g = random.randint(0,255)
        if f>g:
            del party["7"]
            i=1
            while i<7:
                if party[str(i)] != None:
                    del party[str(i)]["participated"]
                i+=1
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party, f_obj, indent=4)
            await ctx.send("Got away safely")
        else:
            party.get("7")["run"]+=1
            await ctx.send("Can't escape")
            if poke1.curhp !=0:
                battle = pokeparty.battle(poke1,poke2)
                if poke2.move4 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3,poke2.move4])
                elif poke2.move3 != None:omove=random.choice([poke2.move1,poke2.move2,poke2.move3])
                elif poke2.move2 != None:omove=random.choice([poke2.move1,poke2.move2])
                else: omove=poke2.move1
                battle.attacks1(move2=omove)
                if poke1.curhp==0:
                    battle.user.status="fainted"
                    if self.whited(party):
                        await ctx.send(poke2.species+" used "+omove.name.title()+". "+effective1+poke1.species+" fainted")
                        await ctx.send("You blacked out")
                        del party["7"]
                    else:
                        await ctx.send(poke2.species+" used "+omove.name.title()+". "+poke1.species+" fainted")
                else:
                    await ctx.send(poke2.species+" used "+omove.name.title())
                party["1"]=battle.user.export()
                result = self.battleBox(party)
                await ctx.send(files=[result[1], result[2]], embed=result[0])
            else:
                party.get("7")["run2"]=1
                result = self.battleBox(party)
                await ctx.send(files=[result[1], result[2]], embed=result[0]) 
            with open("json/parties/"+str(ctx.author.id)+".json", "w") as f_obj:
                json.dump(party, f_obj, indent=4)
    
def setup(bot):
    bot.add_cog(Fight(bot))