import discord
import json
from discord.ext import commands
import os

CONFIG_FILE = "log_channel_ids.json"

def is_guild_manager(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.manage_guild

class LogCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="setup-log", description="Sets up the log channel for message deletions.")
    @discord.app_commands.describe(log_channel_id="The channel ID where logs will be sent.")
    async def log(self, interaction: discord.Interaction, log_channel_id: str):
        if not is_guild_manager(interaction):
            return await interaction.response.send_message("You do not have permission to execute this command. You need manage server permission. 😔", ephemeral=True)

        try:
            guild_id = str(interaction.guild.id)
            log_channel = self.bot.get_channel(int(log_channel_id))

            if not log_channel:
                return await interaction.response.send_message("The channel with this ID was not found. Please check and try again.", ephemeral=True)

            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as file:
                    config_data = json.load(file)
            else:
                config_data = {}

            config_data[guild_id] = log_channel_id

            with open(CONFIG_FILE, "w") as file:
                json.dump(config_data, file, indent=4)

            await interaction.response.send_message(f"The log channel has been set to: {log_channel.mention}", ephemeral=True)

        except Exception:
            await interaction.response.send_message("An error occurred. Try again.", ephemeral=True)
