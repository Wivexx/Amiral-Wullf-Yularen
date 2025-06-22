import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from script.commands.bf2.USEFUL_IDS import (ID_ROLE_JET, ID_ROLE_COMMANDO,
                                            ID_ROLE_FORMATEUR_JET, ID_ROLE_FORMATEUR_COMMANDO,
                                            ID_ROLE_RECRUE_JET, ID_ROLE_RECRUE_COMMANDO,
                                            ID_ROLE_SPECIALITE,
                                            ID_LOGS)

class SpecialiteValidationCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="specialite-validation", description="Utilise cette commande pour valider une specialité.")
    @app_commands.choices(
        recrue=[app_commands.Choice(name=recrue, value=recrue) for recrue in [
            "🛡 Jet-Trooper", "🗡 Commando-Clone"]],
    )
    async def specialite_validation(self, interaction: discord.Interaction, member: discord.Member, recrue: app_commands.Choice[str]):

        user_role = [role for role in interaction.user.roles]
        member_roles = [role for role in member.roles]

        for_recrue_jet = True if recrue.value == "🛡 Jet-Trooper" else False

        if not any(ID_ROLE_FORMATEUR_JET == role.id for role in user_role) and for_recrue_jet:
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_FORMATEUR_JET}> pour utiliser cette commande.",
                ephemeral=True)
        if not any(ID_ROLE_FORMATEUR_COMMANDO == role.id for role in user_role) and not for_recrue_jet:
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_FORMATEUR_COMMANDO}> pour utiliser cette commande.",
                ephemeral=True)

        is_recrue_jet = False
        is_recrue_commando = False
        for role in member_roles:
            if role.id == ID_ROLE_RECRUE_JET: is_recrue_jet = True
            if role.id == ID_ROLE_RECRUE_COMMANDO: is_recrue_commando = True
        if for_recrue_jet and not is_recrue_jet:
            return await interaction.response.send_message(
                f"Vous ne pouvez valider ou non la spécialité que si {member.mention} est <@&{ID_ROLE_RECRUE_JET}>.", ephemeral=True)
        if not for_recrue_jet and not is_recrue_commando:
            return await interaction.response.send_message(
                f"Vous ne pouvez valider ou non la spécialité que si {member.mention} est <@&{ID_ROLE_RECRUE_COMMANDO}>.", ephemeral=True)

        await member.add_roles(interaction.guild.get_role(ID_ROLE_JET if for_recrue_jet else ID_ROLE_COMMANDO))
        await member.add_roles(interaction.guild.get_role(ID_ROLE_SPECIALITE))

        await member.remove_roles(interaction.guild.get_role((ID_ROLE_RECRUE_JET if for_recrue_jet else ID_ROLE_RECRUE_COMMANDO)))

        embed_validation = discord.Embed(title="Spécialité validée",
                                         description=f"{member.mention} a obtenu le rôle <@&{ID_ROLE_JET if for_recrue_jet else ID_ROLE_COMMANDO}>\n"
                                                     "N'oublie pas le messsage à envoyer !\n",
                                         color=discord.Color.green())
        embed_validation.set_footer(text=f"Acceptée par {interaction.user}  •  Message temporaire", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed_validation, ephemeral=True)
        channel = self.bot.get_channel(ID_LOGS)

        return await channel.send(f"{member.mention} a été accepté pour devenir :\n__**{recrue.value}**__\n||<@702493074013814784>||")
