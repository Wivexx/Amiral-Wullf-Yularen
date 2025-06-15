import discord
from discord import app_commands
from discord.ext import commands

from script.commands.bf2.USEFUL_IDS import ID_SESSION_PLAYER, ID_ROLE_LANCEUR, ID_ESCOUADE_HEAD

class CommandeRemoveRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="remove-role-session",
        description="Retire les rôles des participants d'une session."
    )
    async def remove_role_session(self, interaction: discord.Interaction):
        if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
            await interaction.response.send_message(
                f"❌ Vous devez être <@&{ID_ROLE_LANCEUR}> pour utiliser cette commande.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        role_session = interaction.guild.get_role(ID_SESSION_PLAYER)
        role_head = interaction.guild.get_role(ID_ESCOUADE_HEAD)

        removed_session_count = 0
        removed_head_count = 0

        for member in interaction.guild.members:
            try:
                if role_session in member.roles:
                    await member.remove_roles(role_session)
                    removed_session_count += 1
                if role_head in member.roles:
                    await member.remove_roles(role_head)
                    removed_head_count += 1
            except Exception as e:
                print(f"Erreur lors du retrait de rôles pour {member.display_name} : {e}")

        embed = discord.Embed(
            title="🔴 Suppression des rôles de session",
            description=(
                f"→ <@&{ID_SESSION_PLAYER}> retiré de **{removed_session_count}** membre(s)\n"
                f"→ <@&{ID_ESCOUADE_HEAD}> retiré de **{removed_head_count}** membre(s)"
            ),
            color=discord.Color.red()
        )

        await interaction.followup.send(embed=embed, ephemeral=True)
