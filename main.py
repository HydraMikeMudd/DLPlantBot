from core.plant import Plant
import os
from core.sql_engine import SQLEngine
from core.sql_engine import UserDetails
from core.image_loader import load_image_path
from core.image_loader import remove_image_path
import discord
import dotenv

dotenv.load_dotenv()

intents = discord.Intents(messages=True)
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@tree.command(name="share", description="Shares your plant with the server.")
async def show_plant(ctx):
    member_id = ctx.user.id
    guild_id = 0
    if ctx.guild:
        guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_details = conn.get_user(guild_id=guild_id, member_id=member_id)

    if not user_details:
        await ctx.response.send_message("You do not have a plant. Please create one with /show", ephemeral=True)
    elif user_details[UserDetails.IMG_PATH] is None or user_details[UserDetails.GROW] == 1:
        await ctx.response.send_message("Your plant is beginning to grow. Please check back in some time.", ephemeral=True)
    else:
        requester_name = ctx.user.name
        data_stream = load_image_path(user_details[UserDetails.IMG_PATH])
        data_stream.seek(0)
        chart = discord.File(data_stream,filename="plant.png")
        embed = discord.Embed(title=f"{requester_name}'s Plant", color=0x00ff00)
        embed.set_image(url="attachment://plant.png")

        await ctx.response.send_message(embed=embed, file=chart)

@tree.command(name="show", description="Shows only you your plant. If plant does not exist, creates one.")
async def show_plant(ctx):
    member_id = ctx.user.id
    guild_id = 0
    if ctx.guild:
        guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_details = conn.get_user(guild_id=guild_id, member_id=member_id)

    if not user_details:
        plant = Plant(plant_type="random_basic_plant", random=True, random_choices=5)
        plant.grow(4)
        conn.create_new_user(guild_id=guild_id, member_id=member_id, iter=4, curr_string=plant.l_system.current)
        await ctx.response.send_message("Plant has been created and is growing. Please check back in some time.", ephemeral=True)
    elif user_details[UserDetails.IMG_PATH] is None or user_details[UserDetails.GROW] == 1:
        await ctx.response.send_message("Your plant is beginning to grow. Please check back in some time.", ephemeral=True)
    else:
        requester_name = ctx.user.name
        data_stream = load_image_path(user_details[UserDetails.IMG_PATH])
        data_stream.seek(0)
        chart = discord.File(data_stream,filename="plant.png")
        embed = discord.Embed(title=f"{requester_name}'s Plant", color=0x00ff00)
        embed.set_image(url="attachment://plant.png")

        await ctx.response.send_message(embed=embed, file=chart, ephemeral=True)

@tree.command(name="grow", description="Grows your plant by one iteration.")
async def grow_plant(ctx):
    member_id = ctx.user.id
    guild_id = 0
    if ctx.guild:
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
    guild_id = 0
    if ctx.guild:
        guild_id = ctx.guild.id
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")
    user_exists = conn.check_for_user(guild_id=guild_id, member_id=member_id)
    if user_exists:
        user_details = conn.get_user(guild_id=guild_id, member_id=member_id)
        remove_image_path(user_details[UserDetails.IMG_PATH])
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