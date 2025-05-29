import random
import time as t
import discord
from discord.ext import commands
from discord import app_commands

class CommandeBouleMagique(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="boule-magique", description="Donne une réponse à votre question.")
    @app_commands.describe(
        question="Votre question."
    )
    @app_commands.choices(hidden=[
        app_commands.Choice(name="✅", value="true"),
        app_commands.Choice(name="🚫", value="false")
    ])
    async def boule_magique(self, interaction: discord.Interaction, question: str, hidden: str = "false"):
        cache_bool = hidden == "true"
        if question.strip() == "":
            await interaction.response.send_message("❌ Vous devez poser une question.", ephemeral=True)
            return

        reponses_positives = ["Oui", "Certainement", "100% sûr"]
        reponses_negatives = ["Non", "Absolument pas", "Jamais"]
        reponses_neutres = ["Je ne sais pas", "Peut-être", "Repose ta question plus tard", "Impossible de répondre"]
        toutes_les_reponses = reponses_positives + reponses_negatives + reponses_neutres
        reponse = random.choice(toutes_les_reponses)

        t.sleep(1)
        embed = discord.Embed(
            title="🎱 Boule Magique",
            description=f"**Réponse à votre question :**\n*{question}*",
            color=discord.Color.purple()
        )
        embed.add_field(name="Réponse :", value=f"*{reponse}*", inline=False)
        embed.set_footer(text="La Boule Magique sait tout... ou presque !")

        await interaction.response.send_message(embed=embed, ephemeral=cache_bool)
