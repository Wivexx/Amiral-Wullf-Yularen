import discord
from discord import app_commands
from discord.ext import commands
import json
import os

from script.commands.bf2.USEFUL_IDS import ID_SESSION_PLAYER, ID_ANNONCE_SESSION, ID_ROLE_LANCEUR, CHECK_GREEN_REACT, LATE_REACT

SESSION_DATA_FILE = "session_data.json"

class CommandeGiveRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="give-role-session", description="Donner les rôles des participants d'une session.")
    @app_commands.describe(id="ID du message de la session.")
    async def give_role_session(self, interaction: discord.Interaction, id: str):

        if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
            await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_LANCEUR}> pour utiliser cette commande.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        channel = interaction.guild.get_channel(ID_ANNONCE_SESSION)
        try:
            message = await channel.fetch_message(int(id))
        except discord.NotFound:
            await interaction.followup.send("❌ Message introuvable avec cet ID.", ephemeral=True)
            return

        member_ids = set()
        for reaction in message.reactions:
            if reaction.emoji in [CHECK_GREEN_REACT, LATE_REACT]:
                async for user in reaction.users():
                    member = interaction.guild.get_member(user.id)
                    if member and not member.bot:
                        member_ids.add(member.id)

        members = [interaction.guild.get_member(uid) for uid in member_ids if interaction.guild.get_member(uid)]

        role = interaction.guild.get_role(ID_SESSION_PLAYER)
        for member in members:
            try:
                await member.add_roles(role)
            except Exception as e:
                print(f"Erreur lors de l'ajout du rôle à {member.display_name} : {e}")

        session_data = {}
        try:
            if os.path.exists(SESSION_DATA_FILE):
                with open(SESSION_DATA_FILE, "r") as f:
                    session_data = json.load(f)
        except Exception as e:
            print(f"Erreur lecture JSON : {e}")

        session_data[id] = [member.id for member in members]
        try:
            with open(SESSION_DATA_FILE, "w") as f:
                json.dump(session_data, f, indent=4)
        except Exception as e:
            print(f"Erreur écriture JSON : {e}")

        try:
            embed = discord.Embed(
                description=f"✅ Le rôle <@&{ID_SESSION_PLAYER}> a été ajouté à {len(members)} membre(s).",
                color=discord.Color.green()
            )
        except Exception as e:
            embed = discord.Embed(
                description="⚠ Une erreur est survenue. Contactez Wivex.",
                color=discord.Color.red()
            )
            print(f"Erreur embed : {e}")

        await interaction.followup.send(embed=embed, ephemeral=True)
