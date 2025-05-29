import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

class MorpionBouton(Button):
    def __init__(self, x: int, y: int, jeu):
        super().__init__(style=discord.ButtonStyle.secondary, label="⬜", row=y)
        self.x = x
        self.y = y
        self.jeu = jeu

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.jeu.joueur_actuel:
            await interaction.response.send_message("❌ Ce n'est pas votre tour !", ephemeral=True)
            return

        if self.jeu.plateau[self.y][self.x] != "⬜":
            await interaction.response.send_message("❌ Cette case est déjà prise !", ephemeral=True)
            return

        self.jeu.plateau[self.y][self.x] = self.jeu.symbole_actuel
        self.label = self.jeu.symbole_actuel
        self.style = discord.ButtonStyle.green if self.jeu.symbole_actuel == "❌" else discord.ButtonStyle.red
        self.disabled = True
        self.jeu.changer_tour()

        embed = discord.Embed(
            title="🎮 Morpion",
            description=f"## {self.jeu.joueurs[0].mention} vs {self.jeu.joueurs[1].mention}\n-# C'est au tour de {self.jeu.joueur_actuel.mention} !",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Cliquez sur un bouton pour jouer !")

        if self.jeu.verifier_vainqueur():
            for bouton in self.view.children:
                bouton.disabled = True
            embed.description = f"🎉 {interaction.user.mention} a gagné !"
        elif self.jeu.est_match_nul():
            embed.description = "😲 Match nul !"
        else:
            embed.set_footer(text="Cliquez sur un bouton pour jouer !")

        await interaction.response.edit_message(embed=embed, view=self.view)


class MorpionJeu(View):
    def __init__(self, joueur1: discord.User, joueur2: discord.User):
        super().__init__()
        self.plateau = [["⬜"] * 3 for _ in range(3)]
        self.joueurs = [joueur1, joueur2]
        self.joueur_actuel = joueur1
        self.symbole_actuel = "❌"

        for y in range(3):
            for x in range(3):
                self.add_item(MorpionBouton(x, y, self))

    def changer_tour(self):
        self.joueur_actuel = self.joueurs[1] if self.joueur_actuel == self.joueurs[0] else self.joueurs[0]
        self.symbole_actuel = "⭕" if self.symbole_actuel == "❌" else "❌"

    def verifier_vainqueur(self):
        for ligne in self.plateau:
            if ligne[0] == ligne[1] == ligne[2] != "⬜":
                return True

        for col in range(3):
            if self.plateau[0][col] == self.plateau[1][col] == self.plateau[2][col] != "⬜":
                return True

        if self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] != "⬜":
            return True

        if self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] != "⬜":
            return True

        return False

    def est_match_nul(self):
        return all(case != "⬜" for ligne in self.plateau for case in ligne)


class MorpionCommande(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="morpion", description="Jouez à une partie de morpion contre un autre joueur.")
    @app_commands.describe(adversaire="Le joueur contre qui vous voulez jouer.")
    async def morpion(self, interaction: discord.Interaction, adversaire: discord.User):
        if adversaire == interaction.user:
            await interaction.response.send_message("❌ Vous ne pouvez pas jouer contre vous-même !", ephemeral=True)
            return

        if adversaire.bot:
            await interaction.response.send_message("❌ Vous ne pouvez pas jouer contre un bot !", ephemeral=True)
            return

        jeu = MorpionJeu(interaction.user, adversaire)

        embed = discord.Embed(
            title="🎮 Morpion",
            description=f"## {interaction.user.mention} vs {adversaire.mention}\nC'est au tour de {interaction.user.mention} !",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Cliquez sur un bouton pour jouer !")

        await interaction.response.send_message(embed=embed, view=jeu)
