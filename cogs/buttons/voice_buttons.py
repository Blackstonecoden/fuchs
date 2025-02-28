import discord
from discord.ext import commands
from discord import ui
import json

from database.models import VoiceSettings

with open("config.json", 'r', encoding='utf-8') as file:
    config = json.load(file)

class VoiceButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=config["emojis"]["lock"], custom_id="temp_lock_channel", row=0)
    async def lock_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.defer()
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.connect=False
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)

                    settings = await VoiceSettings(interaction.user.id).load()
                    settings.locked = 1
                    await settings.save()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["unlock"], custom_id="temp_unlock_channel", row=1)
    async def unlock_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.defer()
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.connect=True
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)

                    settings = await VoiceSettings(interaction.user.id).load()
                    settings.locked = 0
                    await settings.save()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["eye_off"], custom_id="temp_hide_channel", row=0)
    async def hide_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.defer()
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.read_messages=False
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)

                    settings = await VoiceSettings(interaction.user.id).load()
                    settings.hidden = 1
                    await settings.save()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["eye"], custom_id="temp_unhide_channel", row=1)
    async def unhide_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.defer()
                    channel = self.client.get_channel(channel_id)
                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.read_messages=True
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)
                
                    settings = await VoiceSettings(interaction.user.id).load()
                    settings.hidden = 0
                    await settings.save()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["key"], custom_id="temp_set_exception", row=0)
    async def set_exception_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    view = ExceptionMenuView(self.client, channel_id)
                    await interaction.response.send_message(view=view, ephemeral=True)
                    view.message = await interaction.original_response()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["rotate"], custom_id="temp_reset_exception", row=1)
    async def reset_exception_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    settings = await VoiceSettings(interaction.user.id).load()
                    if settings.exception == 0:
                        await interaction.response.send_message("❌ Der Kanal hat bereits keine Ausnahme.", ephemeral=True)
                        return
                    
                    await interaction.response.defer()
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.get_role(settings.exception)
                    overwrites = channel.overwrites
                    role_overwrites = discord.PermissionOverwrite()
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)

                    settings.exception = 0
                    await settings.save()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["edit"], custom_id="temp_edit_name", row=0)
    async def edit_name_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.send_modal(NameModal(self.client, channel_id))
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["users"], custom_id="temp_member_limit", row=0)
    async def member_limit_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.send_modal(UserLimitModal(self.client, channel_id))
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["user_minus"], custom_id="temp_kick_user", row=1)
    async def kick_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    view = KickMenuView(self.client, channel_id)
                    await interaction.response.send_message(view=view, ephemeral=True)
                    view.message = await interaction.original_response()
                    #await interaction.response.send_message("Soon...",ephemeral=True)
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["trash"], custom_id="temp_delete_channel", row=1)
    async def delete_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    channel = self.client.get_channel(channel_id)
                    await channel.delete()
                    await interaction.response.defer()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)


class NameModal(ui.Modal):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(title="Interface")
        self.client = client
        self.channel_id = channel
    value = discord.ui.TextInput(label="Kanalname", placeholder="Wähle einen neuen Kanalnamen", min_length=2, max_length=50, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = self.client.get_channel(self.channel_id)
        if channel:
            await channel.edit(name=f"🔊｜{self.value.value}")

        settings = await VoiceSettings(interaction.user.id).load()
        settings.name = self.value.value
        await settings.save()


class UserLimitModal(ui.Modal):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(title="Interface")
        self.client = client
        self.channel_id = channel
    value = discord.ui.TextInput(label="Nutzerlimit", placeholder="0-99", min_length=1, max_length=2, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = self.client.get_channel(self.channel_id)
        if channel:
            try:
                value = int(self.value.value)
            except ValueError:
                value = 0
            await channel.edit(user_limit=value)

        settings = await VoiceSettings(interaction.user.id).load()
        settings.limit = self.value.value
        await settings.save()


class KickMenu(discord.ui.UserSelect):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(placeholder="Wähle eine Option aus")
        self.client = client
        self.channel_id = channel

    async def callback(self, interaction: discord.Interaction):
        if str(self.channel_id) in self.client.temp_channels:
            if self.client.temp_channels[str(self.channel_id)]["channel_owner"] == interaction.user.id:
                if self.values[0].id == interaction.user.id:
                    await interaction.response.send_message("❌ Du kannst dich nicht selber kicken.", ephemeral=True)
                    return
                 
                channel = self.client.get_channel(self.channel_id)
                member = channel.guild.get_member(self.values[0].id)
                if member in channel.members:
                    await member.move_to(None)
                    await interaction.response.defer()
                else:
                    await interaction.response.send_message(f"❌ Der Benutzer {member.mention} ist nicht in diesem Kanal.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)


class ExceptionMenu(discord.ui.RoleSelect):
    def __init__(self, client: commands.Bot, channel: discord.VoiceChannel):
        super().__init__(placeholder="Wähle eine Option aus")
        self.client = client
        self.channel_id = channel
    
    async def callback(self, interaction: discord.Interaction):
        if str(self.channel_id) in self.client.temp_channels:
            if self.client.temp_channels[str(self.channel_id)]["channel_owner"] == interaction.user.id:
                await interaction.response.defer()

                channel = self.client.get_channel(self.channel_id)
                overwrites = channel.overwrites
                role_overwrites = overwrites.get(self.values[0], discord.PermissionOverwrite())
                role_overwrites.read_messages=True
                role_overwrites.connect=True
                overwrites[self.values[0]] = role_overwrites
                await channel.edit(overwrites=overwrites)

                settings = await VoiceSettings(interaction.user.id).load()
                settings.exception = self.values[0].id
                await settings.save()
            else:
                await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)


class ExceptionMenuView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(ExceptionMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, ExceptionMenu):
                child.disabled = True
        if self.message:
            await self.message.edit(view=self)


class KickMenuView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(KickMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, KickMenu):
                child.disabled = True
        if self.message:
            await self.message.edit(view=self)


class voice_buttons(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
            
async def setup(client:commands.Bot) -> None:
    await client.add_cog(voice_buttons(client))

