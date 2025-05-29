import random
import discord
from discord import app_commands
from discord.ext import commands

jeux_en_cours = {}


class CommandeTirage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class BoutonParticipation(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, donnees_tirage):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.donnees_tirage = donnees_tirage

        @discord.ui.button(label="Participer", style=discord.ButtonStyle.primary, custom_id="join_button")
        async def rejoindre(self, interaction: discord.Interaction, button: discord.ui.Button):
            utilisateur = interaction.user

            if utilisateur in self.donnees_tirage["participants"]:
                return await interaction.response.send_message("Vous participez déjà au tirage au sort !", ephemeral=True)

            self.donnees_tirage["participants"].append(utilisateur)
            await interaction.response.send_message("Vous avez rejoint le tirage au sort !", ephemeral=True)

            participants_mentions = "\n".join(["- " + p.mention for p in self.donnees_tirage["participants"]]) or "\n*Aucun participant...*\n"
            embed = self.donnees_tirage["message"].embeds[0]
            embed.description = f"\n\n**Récompense :** {self.donnees_tirage['recompense']}\n**Nombre de gagnants :** {self.donnees_tirage['nb_gagnants']}\n\n**┏———— Participants ————┓**\n{participants_mentions}\n"
            embed.set_footer(text=f"Nombre total de participants : {len(self.donnees_tirage['participants'])}")
            await self.donnees_tirage["message"].edit(embed=embed)

        @discord.ui.button(label="Quitter", style=discord.ButtonStyle.danger, custom_id="remove_button")
        async def quitter(self, interaction: discord.Interaction, button: discord.ui.Button):
            utilisateur = interaction.user

            if utilisateur not in self.donnees_tirage["participants"]:
                return await interaction.response.send_message("Vous ne participez pas à ce tirage au sort.", ephemeral=True)

            self.donnees_tirage["participants"].remove(utilisateur)
            await interaction.response.send_message("Vous avez quitté le tirage au sort.", ephemeral=True)

            participants_mentions = "\n".join(["- " + p.mention for p in self.donnees_tirage["participants"]]) or "\n*Aucun participant...*\n"
            embed = self.donnees_tirage["message"].embeds[0]
            embed.description = f"\n\n**Récompense :** {self.donnees_tirage['recompense']}\n**Nombre de gagnants :** {self.donnees_tirage['nb_gagnants']}\n\n**┏———— Participants ————┓**\n{participants_mentions}\n"
            embed.set_footer(text=f"Nombre total de participants : {len(self.donnees_tirage['participants'])}")
            await self.donnees_tirage["message"].edit(embed=embed)

        @discord.ui.button(label="Révéler le gagnant", style=discord.ButtonStyle.success, custom_id="reveal_button")
        async def reveler(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.interaction.user:
                return await interaction.response.send_message("Seul l'organisateur peut révéler les résultats.", ephemeral=True)

            await interaction.response.send_message("Le tirage a été révélé.", ephemeral=True)
            await CommandeTirage.reveler_gagnant(self.interaction)

        def desactiver_boutons(self):
            for item in self.children:
                item.disabled = True

    @app_commands.command(name="tirage", description="Lance un tirage au sort où les utilisateurs peuvent participer et un gagnant est sélectionné.")
    @app_commands.describe(
        recompense="La récompense du tirage.",
        nb_gagnants="Le nombre de gagnants."
    )
    async def tirage(self, interaction: discord.Interaction, recompense: str = "Rien", nb_gagnants: int = 1):
        if interaction.user.id in jeux_en_cours:
            embed = discord.Embed(color=discord.Color.dark_red(), title="Erreur", description=f"{interaction.user.mention}, vous avez déjà un tirage en cours. Révélez le résultat avant d'en créer un autre.")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if nb_gagnants < 1:
            embed = discord.Embed(color=discord.Color.dark_red(), title="Erreur", description="Le nombre de gagnants doit être d'au moins 1.")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="🎉 Tirage au sort 🎉",
            description=f"\n\n**Récompense :** {recompense}\n**Nombre de gagnants :** {nb_gagnants}\n\n**┏———— Participants ————┓**\n*Aucun participant...*\n",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Nombre total de participants : 0")

        message = await interaction.channel.send(embed=embed)

        view = self.BoutonParticipation(interaction, {
            "message": message,
            "participants": [],
            "auteur": interaction.user,
            "recompense": recompense,
            "nb_gagnants": nb_gagnants,
            "jeu_termine": False,
            "vue": None
        })

        jeux_en_cours[interaction.user.id] = view.donnees_tirage
        jeux_en_cours[interaction.user.id]["vue"] = view

        await message.edit(view=view)
        await interaction.response.send_message("Le tirage au sort a commencé !", ephemeral=True)

    @staticmethod
    async def reveler_gagnant(interaction: discord.Interaction):
        if interaction.user.id not in jeux_en_cours:
            embed = discord.Embed(color=discord.Color.dark_red(), title="Erreur", description=f"{interaction.user.mention}, vous n'avez pas de tirage en cours.")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        donnees_tirage = jeux_en_cours.pop(interaction.user.id)

        if donnees_tirage["jeu_termine"]:
            return await interaction.channel.send("Le tirage est déjà terminé.")

        donnees_tirage["jeu_termine"] = True
        vue = donnees_tirage["vue"]

        if vue:
            vue.desactiver_boutons()
            await donnees_tirage["message"].edit(view=vue)

        if not donnees_tirage["participants"]:
            embed = discord.Embed(color=discord.Color.dark_red(), title="Aucun participant", description="Personne n'a participé au tirage.")
            return await interaction.channel.send(embed=embed, reference=donnees_tirage["message"])

        nb_gagnants = donnees_tirage["nb_gagnants"]
        if nb_gagnants > len(donnees_tirage["participants"]):
            embed = discord.Embed(color=discord.Color.dark_red(), title="Erreur", description=f"Le nombre de gagnants ({nb_gagnants}) est supérieur au nombre de participants ({len(donnees_tirage['participants'])}).")
            return await interaction.channel.send(embed=embed, reference=donnees_tirage["message"])

        gagnants = random.sample(donnees_tirage["participants"], nb_gagnants)

        embed_resultats = discord.Embed(
            title="🏆 Résultats du tirage 🏆",
            color=discord.Color.gold(),
            description=f"**Récompense :** {donnees_tirage['recompense']}\n**Nombre de gagnants :** {nb_gagnants}\n\n**┏———— Gagnant(s) ————┓**\n" + "\n".join(["- " + gagnant.mention for gagnant in gagnants])
        )
        embed_resultats.set_footer(text=f"Nombre total de gagnants : {nb_gagnants}")

        message_resultats = await interaction.channel.send(embed=embed_resultats, reference=donnees_tirage["message"])
        await message_resultats.add_reaction("🎉")
