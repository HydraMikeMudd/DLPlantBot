from plant import Plant
import os
from sql_engine import SQLEngine
import discord


intents = discord.Intents(messages=True)
intents.message_content = True #v2
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name='display', description='Displays a plant created randomly.')
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

@tree.command(name="show", description="Shows you your plant. If plant does not exist, creates one.")
async def show_plant(ctx):
    member_id = ctx.user.id
    guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_details = conn.get_user(guild_id=guild_id, member_id=member_id)
    plant = None
    if not user_details:
        plant = Plant(plant_type="random_basic_plant", random=True, random_choices=2)
        plant.grow(4)
        print(guild_id, member_id)
        conn.create_new_user(guild_id=guild_id, member_id=member_id, iter=4, curr_string=plant.l_system.current)
    else:
        plant = Plant(plant_type="random_basic_plant", random=True, random_choices=2, new_start=user_details[1])

    requester_name = ctx.user.name
    data_stream = plant.plot_plant()
    data_stream.seek(0)
    chart = discord.File(data_stream,filename="plant.png")
    embed = discord.Embed(title="Your Plant", color=0x00ff00)
    embed.set_image(url="attachment://plant.png")

    await ctx.response.send_message(embed=embed, file=chart, ephemeral=True)

@tree.command(name="share", description="Shares a random plant with the server.")
async def share_plant(ctx):
    member_id = ctx.user.id
    guild_id = ctx.guild.id
    user_details = await tree.get_user(guild_id, member_id)
    plant = Plant("random_basic_plant", random=True, random_choices=2)
    plant.grow(6)

    requester_name = ctx.user.name
    data_stream = plant.plot_plant()
    data_stream.seek(0)
    chart = discord.File(data_stream,filename="plant.png")
    embed = discord.Embed(title=f"{requester_name} shared their plant!", color=0x00ff00)
    embed.set_image(url="attachment://plant.png")

    await ctx.response.send_message(embed=embed, file=chart)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready")

client.run(os.environ['TOKEN'])