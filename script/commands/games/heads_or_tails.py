import discord
from discord import app_commands
from discord.ext import commands
import random

jeux_en_cours = {}


class CommandePileOuFace(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class VuePileOuFace(discord.ui.View):
        def __init__(self, auteur):
            super().__init__(timeout=None)
            self.pile = []
            self.face = []
            self.auteur = auteur
            self.jeu_termine = False

        @discord.ui.button(label="Pile", style=discord.ButtonStyle.success)
        async def bouton_pile(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.jeu_termine:
                return await interaction.response.send_message("La partie est terminée, vous ne pouvez plus choisir un camp.", ephemeral=True)

            if interaction.user not in self.pile:
                self.pile.append(interaction.user)
            if interaction.user in self.face:
                self.face.remove(interaction.user)

            await self.mettre_a_jour_message(interaction)
            await interaction.response.send_message("Vous avez rejoint l'équipe Pile 🟢", ephemeral=True)

        @discord.ui.button(label="Face", style=discord.ButtonStyle.danger)
        async def bouton_face(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.jeu_termine:
                return await interaction.response.send_message("La partie est terminée, vous ne pouvez plus choisir un camp.", ephemeral=True)

            if interaction.user not in self.face:
                self.face.append(interaction.user)
            if interaction.user in self.pile:
                self.pile.remove(interaction.user)

            await self.mettre_a_jour_message(interaction)
            await interaction.response.send_message("Vous avez rejoint l'équipe Face 🔴", ephemeral=True)

        @discord.ui.button(label="Révéler", style=discord.ButtonStyle.primary)
        async def bouton_reveler(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.auteur:
                return await interaction.response.send_message("Seul l'organisateur peut révéler le résultat.", ephemeral=True)

            if self.jeu_termine:
                return await interaction.response.send_message("La partie est déjà terminée.", ephemeral=True)

            await interaction.response.send_message("Le jeu est terminé.", ephemeral=True)

            self.jeu_termine = True
            self.desactiver_boutons()
            await interaction.message.edit(view=self)

            resultat = random.choice(["pile", "face"])
            gagnants = self.pile if resultat == "pile" else self.face
            gagnants_mentions = "\n".join(["- " + user.mention for user in gagnants]) or "\n*Aucun gagnant...*\n"

            embed = discord.Embed(title="Résultat du Pile ou Face", color=discord.Color.green())
            embed.description = (
                f"Résultat : **{'Pile 🟢' if resultat == 'pile' else 'Face 🔴'}**\n\n"
                f"**┏———— Gagnant(s) ————┓**\n{gagnants_mentions}\n\n"
            )

            message_revelation = await interaction.channel.send(embed=embed, reference=interaction.message)

            if gagnants_mentions != "\n*Aucun gagnant...*\n":
                await message_revelation.add_reaction("🎉")

            if interaction.user.id in jeux_en_cours:
                jeux_en_cours.pop(interaction.user.id)

        async def mettre_a_jour_message(self, interaction: discord.Interaction):
            pile_mentions = "\n".join(["- " + user.mention for user in self.pile]) or "\n*Aucun participant...*\n"
            face_mentions = "\n".join(["- " + user.mention for user in self.face]) or "\n*Aucun participant...*\n"

            embed = interaction.message.embeds[0]
            embed.description = (f"**┏———— Pile 🟢 ————┓**\n{pile_mentions}\n\n"
                                 f"**┏———— Face 🔴 ————┓**\n{face_mentions}")
            await interaction.message.edit(embed=embed)

        def desactiver_boutons(self):
            for child in self.children:
                child.disabled = True

    @app_commands.command(name="pile-ou-face",
                          description="Lance une partie de Pile ou Face où les joueurs peuvent choisir un camp et révéler le résultat.")
    async def pile_ou_face(self, interaction: discord.Interaction):
        if interaction.user.id in jeux_en_cours:
            embed_erreur = discord.Embed(color=discord.Color.dark_red())
            embed_erreur.add_field(
                name=f"{interaction.user.name}, vous avez déjà une partie en cours. Révélez le résultat avant d'en lancer une nouvelle.",
                value="", inline=False)
            await interaction.response.send_message(embed=embed_erreur, ephemeral=True)
            return

        embed = discord.Embed(title="Pile ou Face",
                              description="**┏———— Pile 🟢 ————┓**\n*Aucun participant...*\n\n**┏———— Face 🔴 ————┓**\n*Aucun participant...*\n",
                              color=discord.Color.blue())

        vue = self.VuePileOuFace(interaction.user)
        message = await interaction.response.send_message(embed=embed, view=vue)
        jeux_en_cours[interaction.user.id] = {
            "message": message,
            "vue": vue,
            "auteur": interaction.user
        }
