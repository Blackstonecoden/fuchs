import discord
from discord.ext import commands
from json import load
from easy_pil import Editor, Font, load_image

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

async def generate_welcome_card(user: discord.User, guild: discord.Guild):
    member_count = int(guild.approximate_member_count) or 3

    background = Editor("images/welcome_background.png")

    if user.avatar:
        profile_picture = load_image(str(user.avatar.url))
    else:
        profile_picture = load_image(config["images"]["standard_profile_picture"])
    profile = Editor(profile_picture).resize((150, 150)).circle_image()

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    background.paste(profile, (405, 195))

    background.text(((960/2), 400), f"Willkommen, {user.name}", font=poppins, color="#282828", align="center")
    background.text((15, 500), f"#{(member_count - 2)}", font=poppins_small, color="#e3e3e3ff", align="left")

    return discord.File(fp=background.image_bytes, filename="welcomecard.png")

class join_role(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(config["join_role"])
        if role:
            await member.add_roles(role)

        guild = await self.client.fetch_guild(config["guild_id"])
        file = await generate_welcome_card(member, guild)

        channel: discord.TextChannel  = await self.client.fetch_channel(config["welcome_channel"])
        message = await channel.send(content=f"{member.mention}",file=file)
        await message.add_reaction("🥳")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(join_role(client))