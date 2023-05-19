from plant import Plant
import os

import discord


intents = discord.Intents(messages=True)
intents.message_content = True #v2
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name='display')
async def show_plant(ctx):
    print("Creating Plant")
    plant = Plant("random_basic_plant", random=True, random_choices=2)
    plant.grow(6)

    data_stream = plant.plot_plant()
    data_stream.seek(0)
    chart = discord.File(data_stream,filename="plant.png")
    embed = discord.Embed(title="Your Plant", color=0x00ff00)
    embed.set_image(url="attachment://plant.png")

    await ctx.response.send_message(embed=embed, file=chart, ephemeral=True)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready")

client.run(os.environ['TOKEN'])