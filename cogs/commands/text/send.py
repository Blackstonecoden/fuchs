import discord
from discord.ext import commands
from json import load

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class send_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith("!send "):
            if message.author.guild_permissions.administrator == True:
                await message.delete()
                await message.channel.send(message.content[5:])

async def setup(client:commands.Bot) -> None:
    await client.add_cog(send_command(client))