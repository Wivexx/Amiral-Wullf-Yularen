import random as r
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View

class CommandePierrePapierCiseaux(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="pierre-papier-ciseaux", description="Jouez à Pierre-Papier-Ciseaux contre le bot.")
    @app_commands.choices(hidden=[
        app_commands.Choice(name="✅", value="true"),
        app_commands.Choice(name="🚫", value="false")
    ])
    async def pierre_papier_ciseaux(self, interaction: discord.Interaction, hidden: str = "false"):
        cache_bool = hidden == "true"

        def qui_a_gagne(coup_joueur, coup_bot):
            regles = {
                "pierre": "ciseaux",
                "ciseaux": "papier",
                "papier": "pierre"
            }
            if coup_joueur == coup_bot:
                return "C'est une égalité !"
            return "Tu as gagné ! 🎉" if regles[coup_joueur] == coup_bot else "Tu as perdu... 😢"

        coups_dict = {
            'pierre': {
                'description1': "🪨"
            },
            'papier': {
                'description1': "📄"
            },
            'ciseaux': {
                'description1': "✂️"
            }
        }

        embed = discord.Embed(
            title="🪨 Pierre    📄 Papier    ✂️ Ciseaux",
            description="**Faites votre choix...**",
            color=discord.Color.blue()
        )

        options = [
            discord.SelectOption(
                label=coup.capitalize(),
                description=data['description1'],
                value=coup
            ) for coup, data in coups_dict.items()
        ]

        class SelectionCoup(Select):
            def __init__(self):
                super().__init__(
                    placeholder="Sélectionnez votre coup...",
                    options=options
                )

            async def callback(self, interaction: discord.Interaction):

                coup_joueur = self.values[0]
                coup_bot = r.choice(["pierre", "papier", "ciseaux"])
                resultat = qui_a_gagne(coup_joueur, coup_bot)

                resultat_embed = discord.Embed(
                    title="🪨 Pierre    📄 Papier    ✂️ Ciseaux",
                    description=f"👤 <@{interaction.user.id}> a choisi : **{coup_joueur.capitalize()}**\n👨‍✈️️ <@1357776545124454434> a choisi : **{coup_bot.capitalize()}**",
                    color=discord.Color.blue()
                )
                resultat_embed.add_field(name="**Résultat :**", value=resultat, inline=False)

                await interaction.response.edit_message(embed=resultat_embed, view=None)

        view = View()
        view.add_item(SelectionCoup())

        await interaction.response.send_message(embed=embed, view=view, ephemeral=cache_bool)
