import discord
from discord.ext import commands
from discord import app_commands
import json
from easy_pil import Editor, Font, load_image

from database.models import LevelUser

with open("config.json", 'r', encoding='utf-8') as file:
    config = json.load(file)


async def generate_card(client: commands.Bot, top_users: list) -> discord.File:
    background = Editor("images/leaderboard_background.png")

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)
    poppins_huge = Font.poppins(size=100)

    pos = 1
    for user in top_users:
        discord_user = client.get_user(user[0])
        profile_picture = load_image(str(discord_user.display_avatar))
        user_profile = Editor(profile_picture).resize((70, 70))
        background.paste(user_profile, (0, 70*(pos-1)+(5*(pos-1))))
        background.text((80, (70+5)*(pos-1)+25), f"#{pos} {discord_user.name} • {int((user[1] / 50) ** (1 / 1.5))}", font=poppins_small, color="#282828")
        pos += 1
        

    return discord.File(fp=background.image_bytes, filename="leaderboard.png")
    

class leaderboard_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="leaderboard", description="Zeigt die Top 10 Nutzer an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def level_leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        level_user = await LevelUser(interaction.user.id).load()
        top_users = await level_user.get_top_users()
        file = await generate_card(self.client, top_users)
        embed = discord.Embed(title="Level Leaderboard", color=0x6d6f78)
        embed.set_image(url="attachment://leaderboard.png")
    
        await interaction.edit_original_response(embed=embed, attachments=[file])

async def setup(client:commands.Bot) -> None:
    await client.add_cog(leaderboard_command(client))