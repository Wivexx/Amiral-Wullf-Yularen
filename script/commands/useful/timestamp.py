import discord
import datetime
from discord.ext import commands
from discord import app_commands

class TimestampCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="timestamp", description="Get the Unix timestamp of a given date.")
    @app_commands.describe(
        year="The year.", 
        month="The month (default: 1).", 
        day="The day (default: 1).", 
        hour="The hour (default: 0).", 
        minute="The minute (default: 0).", 
        second="The second (default: 0)."
    )
    async def timestamp(self, interaction: discord.Interaction, year: int, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0, second: int = 0):
        try:
            dt = datetime.datetime(year, month, day, hour, minute, second)
            unix_timestamp = int(dt.timestamp())

            embed = discord.Embed(
                title="⏳ Timestamp Converter",
                description=f"**📅 Date:**\n<t:{unix_timestamp}:F>\n\n**🕒 Unix Timestamp:**\n`{unix_timestamp}`\n\n<t:{unix_timestamp}:R>",
                color=discord.Color.blue()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except ValueError as e:
            await interaction.response.send_message(f"❌ Invalid date: {e}", ephemeral=True)
