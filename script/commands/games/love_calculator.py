import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class CommandeCalculateurAmour(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="calculateur-amour", description="Calcule le pourcentage d'amour entre deux personnes.")
    @app_commands.describe(
        nom_un="Le nom de la première personne.",
        nom_deux="Le nom de la seconde personne."
    )
    @app_commands.choices(hidden=[
        app_commands.Choice(name="✅", value="true"),
        app_commands.Choice(name="🚫", value="false")
    ])
    async def calculateur_amour(self, interaction: discord.Interaction, nom_un: str, nom_deux: str, hidden: str = "true"):
        cache_bool = hidden == "true"
        if not nom_un or not nom_deux:
            await interaction.response.send_message("❌ Vous devez entrer deux noms.", ephemeral=True)
            return

        pourcentage_amour = random.randint(1, 100)

        await interaction.response.defer(ephemeral=cache_bool)

        embed = discord.Embed(
            title="💘 Calculateur d'Amour",
            description="Calcul en cours : **[**░░░░░░░░░░░░░░░░░░░░**]** 0%",
            color=discord.Color.pink()
        )

        message = await interaction.followup.send(embed=embed)

        for pourcentage in range(5, 101, 5):
            await asyncio.sleep(0.4)
            barre_progression = "█" * (pourcentage // 5) + "░" * ((100 - pourcentage) // 5)
            embed.description = f"Calcul en cours : **[**{barre_progression}**]** {pourcentage}%"
            await message.edit(embed=embed)

        await asyncio.sleep(1)
        embed.description = f"**{nom_un.capitalize()}** et **{nom_deux.capitalize()}** ont **{pourcentage_amour}%** d'amour ! 💖"
        await message.edit(embed=embed)

        if pourcentage_amour >= 80: await message.add_reaction("❤️")
        elif pourcentage_amour >= 50: await message.add_reaction("😊")
        elif pourcentage_amour >= 30: await message.add_reaction("😄")
        else: await message.add_reaction("😢")
