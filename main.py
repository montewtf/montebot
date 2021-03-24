import discord
from discord.ext import commands
import random
import logging
import json

#logging.basicConfig(level=logging.DEBUG)

token = open("token.txt", "r").read()
bot = commands.Bot(command_prefix="!")
bot.load_extension("party")
bot.load_extension("misc")
bot.load_extension("fight")

def are_u_monte(ctx):
    return ctx.author.id == 125782351065251840

@bot.command(hidden=True)
@commands.check(are_u_monte)
async def load(ctx, extension):
    bot.load_extension(extension)
    print(extension+" loaded")
    
@bot.command(hidden=True)
@commands.check(are_u_monte)
async def unload(ctx, extension):
    bot.unload_extension(extension)
    print(extension+" unloaded")
    
@bot.command(hidden=True)
@commands.check(are_u_monte)
async def reload(ctx, extension):
    bot.reload_extension(extension)
    print(extension+" reloaded")

bot.run(token)
