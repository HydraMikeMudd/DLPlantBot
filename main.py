from core.plant import Plant
import os
from core.sql_engine import SQLEngine
import discord
import dotenv

dotenv.load_dotenv()

intents = discord.Intents(messages=True)
intents.message_content = True #v2
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)



@tree.command(name="show", description="Shows you your plant. If plant does not exist, creates one.")
async def show_plant(ctx):
    member_id = ctx.user.id
    guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_details = conn.get_user(guild_id=guild_id, member_id=member_id)
    plant = None

    await ctx.response.defer()

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
    embed = discord.Embed(title=f"{requester_name}'s Plant", color=0x00ff00)
    embed.set_image(url="attachment://plant.png")

    await ctx.followup.send(embed=embed, file=chart, ephemeral=True)

@tree.command(name="grow", description="Grows your plant by one iteration.")
async def grow_plant(ctx):
    member_id = ctx.user.id
    guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_details = conn.get_user(guild_id=guild_id, member_id=member_id)
    if not user_details:
        await ctx.response.send_message("You do not have a plant. Please create one with /show", ephemeral=True)
        return
    elif user_details[0] > 6:
        await ctx.response.send_message("Your plant is fully grown.", ephemeral=True)
    else:
        conn.set_user_grow(guild_id=guild_id, member_id=member_id)
        await ctx.response.send_message("Your plant is beginning to grow. Check back in some time.", ephemeral=True)
        return

@tree.command(name="delete", description="Deletes your existing plant.")
async def reset_plant(ctx):
    member_id = ctx.user.id
    guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_exists = conn.check_for_user(guild_id=guild_id, member_id=member_id)
    if user_exists:
        conn.delete_user(guild_id=guild_id, member_id=member_id)
        await ctx.response.send_message("Your plant has been deleted.", ephemeral=True)
        return
    else:
        await ctx.response.send_message("You do not have a plant. Please create one with /show", ephemeral=True)
        return


@client.event
async def on_ready():
    await tree.sync()
    print("Ready")

client.run(os.environ["DISCORD_TOKEN"])