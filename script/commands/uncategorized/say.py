import discord
from discord.ext import commands

class SayCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="say", description="Makes the bot speak with the message you provide.")
    @discord.app_commands.describe(message="The message that the bot should repeat.")
    async def say(self, interaction: discord.Interaction, message: str):
        try:
            await interaction.channel.send(message + f"\n-# {interaction.user.name} made me say this.")
        except Exception:
            await interaction.response.send_message("The message couldn't be delivered... I'm sorry 😔")
