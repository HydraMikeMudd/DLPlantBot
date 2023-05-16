from plant import Plant
import os

import discord
from discord.ext import commands

intents = discord.Intents(messages=True)
intents.message_content = True #v2
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='display')
async def show_plant(ctx):
    print("Creating Plant")
    plant = Plant("random_basic_plant", random=True, random_choices=2)
    plant.grow(5)

    data_stream = plant.plot_plant()
    data_stream.seek(0)
    chart = discord.File(data_stream,filename="plant.png")
    embed = discord.Embed(title="Your Plant", color=0x00ff00)
    embed.set_image(url="attachment://temp_plant.png")

    await ctx.send(embed=embed, file=chart)

bot.run(os.environ['DISCORD_TOKEN'])