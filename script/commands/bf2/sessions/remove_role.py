import discord
from discord import app_commands
from discord.ext import commands
import json
import os

from script.commands.bf2.USEFUL_IDS import ID_SESSION_PLAYER, ID_ROLE_LANCEUR

SESSION_DATA_FILE = "session_data.json"

class CommandeRemoveRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="remove-role-session", description="Retirer le rôle des participants d'une session enregistrée.")
    @app_commands.describe(id="ID du message de la session.")
    async def remove_role_session(self, interaction: discord.Interaction, id: str):
        if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
            await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_LANCEUR}> pour utiliser cette commande.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            if not os.path.exists(SESSION_DATA_FILE):
                await interaction.followup.send("❌ Aucun fichier de session trouvé.", ephemeral=True)
                return

            with open(SESSION_DATA_FILE, "r") as f:
                session_data = json.load(f)

            if id not in session_data:
                await interaction.followup.send("❌ Aucun participant enregistré pour cet ID de session.", ephemeral=True)
                return
        except Exception as e:
            await interaction.followup.send("❌ Erreur lors de la lecture du fichier JSON.", ephemeral=True)
            print("Erreur lecture JSON :", e)
            return

        member_ids = session_data[id]
        role = interaction.guild.get_role(ID_SESSION_PLAYER)
        count = 0

        for uid in member_ids:
            member = interaction.guild.get_member(uid)
            if member and role in member.roles:
                try:
                    await member.remove_roles(role)
                    count += 1
                except Exception as e:
                    print(f"Erreur lors du retrait du rôle pour {member.display_name} : {e}")

        try:
            del session_data[id]
            with open(SESSION_DATA_FILE, "w") as f:
                json.dump(session_data, f, indent=4)
        except Exception as e:
            await interaction.followup.send("⚠ Erreur lors de l'enregistrement du fichier.", ephemeral=True)
            print("Erreur écriture JSON :", e)
            return

        embed = discord.Embed(
            description=f"🔴 Le rôle <@&{ID_SESSION_PLAYER}> a été retiré à {count} membre(s).",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
