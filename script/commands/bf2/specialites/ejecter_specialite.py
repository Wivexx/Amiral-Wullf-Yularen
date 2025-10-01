import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from USEFUL_IDS import (ID_ROLE_FORMATEUR_JET, ID_ROLE_FORMATEUR_COMMANDO, ID_ROLE_INSTRUCTEUR,
                        ID_ROLE_SPECIALITE, ID_ROLE_JET, ID_ROLE_COMMANDO,
                        ID_ROLE_RECRUE_JET, ID_ROLE_RECRUE_COMMANDO,
                        ID_ROLE_DOUBLE_SPE)

class EjecterSpecialiteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ejecter-specialite", description="Utilise cette commande pour éjecter quelqu'un d'une spécialité.")
    @app_commands.choices(
        specialite=[
            app_commands.Choice(name="🛡 Jet-Trooper", value=1),
            app_commands.Choice(name="🗡 Commando Clone", value=0)
        ]
    )
    async def ejecter_specialite(self, interaction: discord.Interaction, member: discord.Member, specialite: app_commands.Choice[int]):

        user_role = interaction.user.roles

        if not any(ID_ROLE_FORMATEUR_JET == role.id for role in user_role) and specialite.value == 1:
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_FORMATEUR_JET}> pour utiliser cette commande.",
                ephemeral=True)
        if not any(ID_ROLE_FORMATEUR_COMMANDO == role.id for role in user_role) and specialite.value == 0:
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_FORMATEUR_COMMANDO}> pour utiliser cette commande.",
                ephemeral=True)

        if not any(ID_ROLE_SPECIALITE == role.id for role in member.roles):
            return await interaction.response.send_message(
                f"{member.mention} ne fait parti d'aucune spécialité.",
                ephemeral=True)

        is_jet = False
        is_commando = False
        for role in member.roles:
            if role.id == ID_ROLE_RECRUE_JET or role.id == ID_ROLE_JET: is_jet = True
            if role.id == ID_ROLE_RECRUE_COMMANDO or role.id == ID_ROLE_COMMANDO: is_commando = True
        if specialite == 1 and not is_jet:
            return await interaction.response.send_message(
                f"Vous ne pouvez retirer la spécialité que si {member.mention} est <@&{ID_ROLE_RECRUE_JET}> ou <@&{ID_ROLE_JET}>.",
                ephemeral=True)
        if specialite == 0 and not is_commando:
            return await interaction.response.send_message(
                f"Vous ne pouvez retirer la spécialité que si {member.mention} est <@&{ID_ROLE_RECRUE_COMMANDO}> ou <@&{ID_ROLE_COMMANDO}>.",
                ephemeral=True)

        if not any(ID_ROLE_DOUBLE_SPE == role.id for role in member.roles):
            await member.remove_roles(interaction.guild.get_role(ID_ROLE_SPECIALITE))

        if specialite.value:
            await member.remove_roles(interaction.guild.get_role(ID_ROLE_RECRUE_JET))
            await member.remove_roles(interaction.guild.get_role(ID_ROLE_JET))
        else:
            await member.remove_roles(interaction.guild.get_role(ID_ROLE_RECRUE_COMMANDO))
            await member.remove_roles(interaction.guild.get_role(ID_ROLE_COMMANDO))

        await member.remove_roles(interaction.guild.get_role(ID_ROLE_DOUBLE_SPE))

        embed = discord.Embed(title="Éjecté de la spécialité",
                                description=f"{member.mention} a perdu sa spécialité {"Jet-Trooper" if specialite.value == 1 else "Commando Clone"}.",
                                color=discord.Color.red())
        embed.set_footer(text=f"Éjecté par {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(f"{member.mention}", embed=embed)

