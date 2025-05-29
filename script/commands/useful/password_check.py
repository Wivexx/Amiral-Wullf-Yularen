import requests
import discord
import hashlib
from discord.ext import commands
from discord import app_commands


class PasswordCheckCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="password-check",
                          description="Check if a password has been compromised in a data breach.")
    @app_commands.describe(password="Password to check if it has been compromised.")
    async def passwordcheck(self, interaction: discord.Interaction, password: str):

        sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_password[:5]
        suffix = sha1_password[5:]

        try:
            response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')

            embed = discord.Embed(color=discord.Color.dark_red())

            result_message = "**[ ! ]** This password has been compromised." if suffix in response.text else "**[+]** This password has not been found in any data breaches."

            embed.add_field(name="Result:", value=result_message, inline=False)

            embed.set_footer(text="Data provided by PwnedPasswords")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)