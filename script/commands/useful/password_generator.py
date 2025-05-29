import random
import discord
from discord.ext import commands
from discord import app_commands
class PasswordGeneratorCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="password-generator", description="Generate a strong random password with the specified length.")
    @app_commands.describe(length="Length of the password to generate (min: 1, max: 128).")
    async def password_generator(self, interaction: discord.Interaction, length: int):
        if length < 1 or length > 128: return await interaction.response.send_message("❌ Password length must be between 1 and 128.", ephemeral=True)
        await interaction.response.send_message(f"## 🔐 Generated password :\n||```{"".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>?/") for i in range(length))}```||", ephemeral=True)