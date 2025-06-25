import discord
from discord import app_commands
from discord.ext import commands

from USEFUL_IDS import (
    ID_SESSION_PLAYER,
    ID_ANNONCE_SESSION,
    ID_ROLE_LANCEUR,
    ID_ESCOUADE_HEAD,
    CHECK_GREEN_REACT,
    LATE_REACT
)

class CommandeGiveRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="give-role-session",
        description="Donne les rôles session + chef d’escouade."
    )
    @app_commands.describe(
        id="ID du message de la session.",
        chefs_escouades="Mentionne les chefs d’escouade."
    )
    async def give_role_session(self, interaction: discord.Interaction, id: str, chefs_escouades: str):
        if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
            await interaction.response.send_message(
                f"❌ Vous devez être <@&{ID_ROLE_LANCEUR}> pour utiliser cette commande.",
                ephemeral=True
            )
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
        role_player = interaction.guild.get_role(ID_SESSION_PLAYER)
        role_head = interaction.guild.get_role(ID_ESCOUADE_HEAD)

        count_player, count_head = 0, 0
        failed_players, failed_heads = [], []

        for member in members:
            try:
                await member.add_roles(role_player)
                count_player += 1
            except Exception:
                failed_players.append(member.display_name)

        for member in interaction.guild.members:
            if f"<@{member.id}>" in chefs_escouades or f"<@!{member.id}>" in chefs_escouades:
                try:
                    await member.add_roles(role_head)
                    count_head += 1
                except Exception:
                    failed_heads.append(member.display_name)
        title = f"🟢 Ajout des rôles de session\n"
        desc = (
            f"→ <@&{ID_SESSION_PLAYER}> ajouté à **{count_player}** membre(s)\n"
            f"→ <@&{ID_ESCOUADE_HEAD}> ajouté à **{count_head}** membre(s)"
        )
        if failed_players:
            desc += f"\n⚠ Erreurs (joueurs) : {' - '.join(failed_players)}"
        if failed_heads:
            desc += f"\n⚠ Erreurs (chefs) : {' - '.join(failed_heads)}"

        embed = discord.Embed(title=title, description=desc, color=discord.Color.green())
        await interaction.followup.send(embed=embed, ephemeral=True)
