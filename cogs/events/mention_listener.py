import discord
from discord.ext import commands
from json import load

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

class mention_listener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.content == f"<@&{config["suggestion_role"]}>" and message.reference:
            await message.delete()
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            await referenced_message.add_reaction("✅")
            await referenced_message.add_reaction("👍")
            await referenced_message.add_reaction("👎")
            await referenced_message.add_reaction("❌")
        elif f"<@&{config["suggestion_role"]}>" in message.content:
            await message.add_reaction("✅")
            await message.add_reaction("👍")
            await message.add_reaction("👎")
            await message.add_reaction("❌")
        elif any(f"<@{mention}>" in message.content for mention in config["ping_reactions"]):
            id = next((mention for mention in config["ping_reactions"] if f"<@{mention}>" in message.content), None)
            await message.add_reaction(config["ping_reactions"][id])

async def setup(client:commands.Bot) -> None:
    await client.add_cog(mention_listener(client))