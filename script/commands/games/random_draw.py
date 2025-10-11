import discord
from discord.ext import commands
from discord import app_commands
import random

class RandomDrawCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="tirage-aleatoire",
        description="Tire un nombre de participants parmi les membres d’un rôle sélectionné."
    )
    @app_commands.describe(
        role="Le rôle parmi lequel effectuer le tirage.",
        nombre="Nombre de personnes à tirer."
    )
    async def random_draw(self, interaction: discord.Interaction, role: discord.Role, nombre: int):
        if len(role.members) < nombre:
            return await interaction.response.send_message(
                f"❌ Le nombre de personnes tirées ne peut pas être supérieur au nombre de membres possédant le rôle {role.mention}.",
                ephemeral=True
            )

        selected = random.sample(role.members, nombre)

        embed = discord.Embed(
            title="👥 Membres tirés",
            description=(
                f"Tirage parmi les membres possédant le rôle {role.mention}\n"
                + ("\n".join(["- " + member.mention for member in selected]) or "\n*Aucun participant...*\n")
            ),
            color=role.color
        )

        await interaction.response.send_message(embed=embed)
