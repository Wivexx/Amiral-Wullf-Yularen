import discord
from discord.ext import commands
import re

class ManageRoleCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="gerer-role", description="Ajoute/retirer un rôle à plusieurs personnes en même temps.")
    @discord.app_commands.describe(role="Le rôle à ajouter/retirer.", membres="Mentionnez plusieurs membres séparés par un espace.")
    @discord.app_commands.choices(action=[
        discord.app_commands.Choice(name="✅ Ajouter", value=1),
        discord.app_commands.Choice(name="❌ Retirer", value=0)
    ])
    async def add_role(self, interaction: discord.Interaction, action: int, role: discord.Role, membres: str):
        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("Seuls les modérateurs peuvent utiliser cette commande.", ephemeral=True)

        member_ids = re.findall(r"<@!?(\d+)>", membres)
        if not member_ids:
            return await interaction.response.send_message("⚠️ Vous devez mentionner au moins un membre.", ephemeral=True)

        members_to_edit = []
        for member_id in member_ids:
            member = interaction.guild.get_member(int(member_id))
            if member:
                members_to_edit.append(member)

        if not members_to_edit:
            return await interaction.response.send_message("⚠️ Aucun membre valide trouvé dans vos mentions.", ephemeral=True)

        for member in members_to_edit:
            if action: await member.add_roles(role, reason=f"Rôle ajouté grâce à /gerer-role par {interaction.user}.")
            else: await member.remove_roles(role, reason=f"Rôle retiré grâce à /gerer-role par {interaction.user}.")


        embed = discord.Embed(color=discord.Color.green() if action else discord.Color.red())
        embed.add_field(
            name="Ajout de rôle" if action else "Retrait de rôle",
            value=f"✅ Le rôle {role.mention} a été {"ajouté" if action else "retiré"} à {len(members_to_edit)} personne(s).",
            inline=False
        )

        await interaction.response.send_message(embed=embed)
