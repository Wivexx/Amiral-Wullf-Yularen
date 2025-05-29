import random
import discord
from discord import app_commands
from discord.ext import commands

class CommandeNombreAleatoire(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="nombre-aleatoire", description="Génère un nombre aléatoire entre 1 et votre nombre choisi.")
    @app_commands.describe(nombre_max="Entrez le nombre maximum")
    @app_commands.choices(hidden=[
        app_commands.Choice(name="✅", value="true"),
        app_commands.Choice(name="🚫", value="false")
    ])
    async def nombre_aleatoire(self, interaction: discord.Interaction, nombre_max: int, hidden: str = "false"):
        cache_bool = hidden == "true"
        if nombre_max < 1:
            await interaction.response.send_message("❌ Le nombre doit être supérieur à 0.", ephemeral=True)
            return

        nombre_choisi = random.randint(1, nombre_max)

        embed = discord.Embed(
            title="🎲 Générateur de Nombre Aléatoire",
            description=f"Le nombre choisi est : **{nombre_choisi}**",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=cache_bool)
