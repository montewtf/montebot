import discord
from discord.ext import commands
import random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("with your <3"))
        print("We have logged in as {0.user}".format(self.bot))                
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message):
            await message.channel.send("Hi "+message.author.mention)
            
    @commands.command()
    async def burn(self, ctx):
        await ctx.send("https://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States")

    @commands.command()
    async def raffle(self, ctx, *slist):
        raffle = list()
        i=0
        while i<len(slist):
            index = slist[i]
            i+=1
            person = index[:index.find("-")]
            tickets = int(index[index.find("-")+1:])
            j=0
            while j<tickets:
                raffle.append(person)
                j+=1
        winner = raffle[random.randint(0,len(raffle)-1)]
        await ctx.send("Congrats! "+winner+" has won the raffle")

def setup(bot):
    bot.add_cog(Misc(bot))