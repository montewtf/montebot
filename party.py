import discord
from discord.ext import commands
import json
import asyncio
import pokeparty

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def party(self, ctx):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        if party == None:
            await ctx.send("You have to pick a starter first")
            return
        embed=discord.Embed(title="Party", color=discord.Color.blue())
        i=1
        while i<7:
            p = party.get(str(i))
            if p == None:
                embed.add_field(name=str(i), value="Empty", inline=False)
            if p != None:
                if p.get("name")==None:
                    embed.add_field(name=str(i), value=p.get("species")+" Lvl: "+str(p.get("level")), inline=False)
                else:
                    embed.add_field(name=str(i), value=p.get("name")+" ("+p.get("species")+") Lvl: "+str(p.get("level")), inline=False)
            i+=1
        await ctx.send(embed=embed)

    @commands.command()
    async def summary(self, ctx, slot):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        party = dic.get(str(ctx.author.id))
        if party == None:
            await ctx.send("You have to pick a starter first")
            return
        p=party.get(str(slot))
        file=discord.File("thumbnails/"+p.get("id")+".png", filename="image.png")
        embed=discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url="attachment://image.png")
        if p.get("name")==None:
            embed.add_field(name="Pokemon", value=p.get("species"), inline=True)
        else:
            embed.add_field(name="Pokemon", value=p.get("name")+" ("+p.get("species")+")", inline=True)
        embed.add_field(name="Level", value=p.get("level"), inline=True)
        if len(p.get("types"))==2:
            types = p.get("types")
            embed.add_field(name="Types", value=types[0]+", "+types[1], inline=False)
        else:
            embed.add_field(name="Type", value=p.get("types")[0], inline=False)
        stats = p.get("stats")
        moves = p.get("moves")
        with open("json/moves.json") as f_obj:
            moves2 = json.load(f_obj)
        embed.add_field(name="HP", value=str(stats.get("Current HP"))+"/"+str(stats.get("HP")), inline=False)
        embed.add_field(name="Attack", value=stats.get("Attack"), inline=True)
        embed.add_field(name="Defense", value=stats.get("Defense"), inline=True)
        embed.add_field(name="Special", value=stats.get("Special"), inline=True)
        embed.add_field(name="Speed", value=stats.get("Speed"), inline=True)
        embed2=discord.Embed(title="Moves")
        embed2.add_field(name=moves.get("move1"), value="-", inline=True)
        embed2.add_field(name=moves.get("move2"), value="-", inline=True)
        embed2.add_field(name="\u200B", value="\u200B", inline=True)
        embed2.add_field(name=moves.get("move3"), value="-", inline=True)
        embed2.add_field(name=moves.get("move4"), value="-", inline=True)
        embed2.add_field(name="\u200B", value="\u200B", inline=True)
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
        new = pokeparty.pokemon(poke, level, name=name)
        poke = new.export()
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        if dic.get(str(ctx.author.id)) == None:
            await ctx.send("You have to pick a starter first")
            return
        currentp = pokeparty.party(dic.get(str(ctx.author.id)))
        add = currentp.add(poke)
        if not add:
            await ctx.send("Your party is full")
            return
        dic[str(ctx.author.id)] = currentp.recon()
        await ctx.send("Pokemon added to slot: "+str(add))     
        with open("json/parties.json", "w") as f_obj:
            json.dump(dic, f_obj, indent=4)

    @commands.command()
    async def release(self, ctx, slot):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        if dic.get(str(ctx.author.id)) == None:
            await ctx.send("You have no Pokemon")
            return
        currentp = pokeparty.party(dic.get(str(ctx.author.id)))
        if currentp.remove(int(slot)):
            await ctx.send("Invalid slot")
            return
        msg = await ctx.send("Are you sure you want to delete the pokemon in slot "+slot+"? (y/n)")
        def yes(m):
            return m.author == ctx.author
        try:
            answer = await bot.wait_for("message", check=yes, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out")
        if answer.content.lower() == "y" or answer.content.lower() == "yes":
            await ctx.send("Pokemon released")
            dic[str(ctx.author.id)] = currentp.recon()
            with open("json/parties.json", "w") as f_obj:
                json.dump(dic, f_obj, indent=4)
        elif answer.content.lower() == "n" or answer.content.lower() == "no":
            await ctx.send("Release cancelled")
        else:
            await ctx.send("Invalid answer")
        
    @commands.command()
    async def swap(self, ctx, slot1, slot2):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        if dic.get(str(ctx.author.id)) == None:
            await ctx.send("You have to pick a starter first")
            return
        currentp = pokeparty.party(dic.get(str(ctx.author.id)))
        if currentp.swap(int(slot1), int(slot2)):
            await ctx.send("Invalid slots")
            return
        dic[str(ctx.author.id)] = currentp.recon()
        await ctx.send("Pokemon "+slot1+" & "+slot2+" have been swapped")
        with open("json/parties.json", "w") as f_obj:
            json.dump(dic, f_obj, indent=4)

    @commands.command()
    async def starter(self, ctx, starter, name=None):
        with open("json/parties.json") as f_obj:
            dic = json.load(f_obj)
        with open("json/pokedex.json") as f_obj:
            dex = json.load(f_obj)
        if str(ctx.author.id) in dic:
            await ctx.send("You have already picked a starter")
        elif starter.lower() in ("squirtle","charmander","bulbasaur"):
            for i in (0,3,6):
                poke = dex[i]
                if starter.capitalize() == poke["name"]:
                    break
            new = pokeparty.pokemon(poke, 5, name=name)
            poke = new.export()
            dic[str(ctx.author.id)] = {"1":poke,"2":None,"3":None,"4":None,"5":None,"6":None,}
            with open("json/parties.json", "w") as f_obj:
                json.dump(dic, f_obj, indent=4)
            await ctx.send("You have obtained "+str(starter).capitalize()+"!")
            
    @commands.command(hidden = True)
    async def wild(self, ctx):
        with open("json/parties.json") as f_obj:
            parties = json.load(f_obj)
        party = parties.get(str(ctx.author.id))
        checker = False
        if "7" not in party:
            checker = True
            with open("json/pokedex.json") as f_obj:
                dex = json.load(f_obj)
            i=0
            while i<151:
                poke = dex[i]
                if "Rattata" == poke["name"]:
                    break
                i+=1
            battle = pokeparty.pokemon(poke, 2)
            party["7"] = battle.export()
            parties[str(ctx.author.id)] = party
            with open("json/parties.json", "w") as f_obj:
                json.dump(parties, f_obj, indent=4)
        battle=party.get("7")
        file=discord.File("thumbnails/"+battle.get("id")+".png", filename="image.png")
        embed=discord.Embed(title=battle.get("species")+" Lv."+str(battle.get("level")), description=str(battle.get("Current HP"))+"/"+str(battle.get("HP")))
        embed.set_thumbnail(url="attachment://image.png")
        embed.add_field(name="!fight", value="\u200B", inline=True)
        embed.add_field(name="!pokemon", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        embed.add_field(name="!catch", value="\u200B", inline=True)
        embed.add_field(name="!run", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        first = party.get("1")
        file2=discord.File("thumbnails/"+first.get("id")+".png", filename="image2.png")
        embed.set_image(url="attachment://image2.png")
        if first.get("name")==None:
            embed.set_footer(text=first.get("species")+" Lv."+str(first.get("level"))+" "+str(first.get("stats").get("Current HP"))+"/"+str(first.get("stats").get("HP")))
        else:
            embed.set_footer(text=first.get("name")+" Lv."+str(first.get("level"))+" "+str(first.get("stats").get("Current HP"))+"/"+str(first.get("stats").get("HP")))
        if checker:
            await ctx.send("Wild "+battle.get("species")+" appeared!", files=[file, file2], embed=embed)
        else:
            await ctx.send("Already in battle", files=[file, file2], embed=embed)
        
def setup(bot):
    bot.add_cog(Pokemon(bot))