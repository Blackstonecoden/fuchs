import discord
from discord.ext import commands
import json
import random

from database.models import VoiceSettings

with open("config.json", 'r', encoding='utf-8') as file:
    config = json.load(file)



class voice_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.temp_channels = {}

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        category = self.client.get_channel(config["categories"]["temp_channels"])
        if category is not None and isinstance(category, discord.CategoryChannel):
            for channel in category.voice_channels:
                if channel.id != config["channels"]["temp_join"]:
                    await channel.delete()

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None and after.channel != before.channel:
            if after.channel.id == config["channels"]["temp_join"]:
                category = self.client.get_channel(config["categories"]["temp_channels"])
                settings = await VoiceSettings(member.id).load()

                overwrites = {}
                overwrites[member.guild.default_role] = discord.PermissionOverwrite(send_messages=True, attach_files=True, embed_links=True, add_reactions=True)
                if settings.locked == 1:
                    overwrites[member.guild.default_role].connect = False
                if settings.hidden == 1:
                    overwrites[member.guild.default_role].read_messages = False
                if settings.exception != 0:
                    overwrites[member.guild.get_role(settings.exception)] = discord.PermissionOverwrite(read_messages = True, connect = True)

                if settings.name:
                    temp_channel = await category.create_voice_channel(name=f"🔊｜{settings.name}", user_limit=settings.limit, overwrites=overwrites)
                else:
                    temp_channel = await category.create_voice_channel(name="🔊｜Temp Kanal", user_limit=settings.limit, overwrites=overwrites)    
                await member.move_to(temp_channel)
                self.client.temp_channels[str(temp_channel.id)] = {"channel_owner": member.id}

        if before.channel is not None and after.channel != before.channel:
            try:
                channel_id = before.channel.id
                if str(channel_id) in self.client.temp_channels:
                    if self.client.temp_channels[str(channel_id)]["channel_owner"] == member.id:
                        if len(before.channel.members) == 0:
                            await before.channel.delete()
                            del self.client.temp_channels[str(channel_id)]
                        else:
                            random_member = random.choice(before.channel.members)
                            self.client.temp_channels[str(channel_id)]["channel_owner"] = random_member.id
            except:
                return
            


async def setup(client:commands.Bot) -> None:
    await client.add_cog(voice_system(client))