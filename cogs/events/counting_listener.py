import discord
from discord.ext import commands
from json import load, dump

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

def save_to_json(location, content):
    with open(location, 'w') as file:
        dump(content, file, indent=4)

class counting_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id == config["channels"]["counting"]:
            if message.author.id != self.client.storage["counting_last_user"]:
                if message.content == str(self.client.storage["counting_current_number"]):
                    self.client.storage["counting_current_number"] += 1
                    self.client.storage["counting_last_user"] = message.author.id
                    if (self.client.storage["counting_current_number"]-1)%1000 == 0:
                        await message.add_reaction("🏆") 
                    elif (self.client.storage["counting_current_number"]-1)%100 == 0:
                        await message.add_reaction("☑") 
                    else:
                        await message.add_reaction("✅")
                    save_to_json("json/data.json", self.client.storage)
                else:
                    await message.delete()
            else:
                await message.delete()

async def setup(client:commands.Bot) -> None:
    await client.add_cog(counting_system(client))