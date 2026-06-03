import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from USEFUL_IDS import (ID_ROLE_FORMATEUR_JET, ID_ROLE_FORMATEUR_COMMANDO,
                        ID_ROLE_RECRUE_JET, ID_ROLE_RECRUE_COMMANDO,
                        ID_ROLE_CRA, ID_ROLE_COMMANDO, ID_ROLE_JET,
                        ID_ROLE_SPECIALITE, ID_ROLE_DOUBLE_SPE,
                        ID_ROLE_GARDE,
                        ID_LOGS, ID_ROLE_APPRENTI_FORMATEUR, ID_POLE_SPE)

class CandidatureSpecialiteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="candidature-specialite", description="Utilise cette commande pour accepter ou refuser une candidature pour une specialité.")
    @app_commands.choices(
        validation=[
        app_commands.Choice(name="✅ Candidature acceptée", value=1),
        app_commands.Choice(name="🚫 Candidature refusée", value=0)],
        recrue=[app_commands.Choice(name=recrue, value=recrue) for recrue in [
            "🛡 Recrue Jet-Trooper", "🗡 Recrue Commando-Clone"]],
    )
    @app_commands.describe(raison="/!\\ Raison SI REFUS /!\\")
    async def candidature_specialite(self, interaction: discord.Interaction, member: discord.Member, validation:int, recrue: app_commands.Choice[str],  raison: str = ""):

        user_role = [role for role in interaction.user.roles]

        """is_recrue_jet = True if recrue.value == "🛡 Recrue Jet-Trooper" else False

        if not any(ID_ROLE_FORMATEUR_JET == role.id or ID_ROLE_APPRENTI_FORMATEUR == role.id for role in user_role) and is_recrue_jet:
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_FORMATEUR_JET}> ou <@&{ID_ROLE_APPRENTI_FORMATEUR}> pour utiliser cette commande.",
                ephemeral=True)
        if not any(ID_ROLE_FORMATEUR_COMMANDO == role.id or ID_ROLE_APPRENTI_FORMATEUR == role.id for role in user_role) and not is_recrue_jet:
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_FORMATEUR_COMMANDO}> ou <@&{ID_ROLE_APPRENTI_FORMATEUR}> pour utiliser cette commande.",
                ephemeral=True)
        """

        if not any(ID_POLE_SPE == role.id for role in user_role):
            return await interaction.response.send_message(
            f"❌ Vous devez faire parti du pôle spécialité pour utiliser cette commande.", ephemeral=True)

        if validation:
            member_roles = member.roles
            role_ids = [role.id for role in member_roles]

            has_garde = ID_ROLE_GARDE in role_ids
            has_commando = ID_ROLE_RECRUE_COMMANDO in role_ids or ID_ROLE_COMMANDO in role_ids
            has_jet = ID_ROLE_JET in role_ids or ID_ROLE_RECRUE_JET in role_ids
            has_cra = ID_ROLE_CRA in role_ids

            if (has_jet and is_recrue_jet) or (has_commando and not is_recrue_jet):
                return await interaction.response.send_message(
                    f"{member.mention} possède déjà la spécialité.",
                    ephemeral=True)

            if not has_garde and (has_commando or has_jet or has_cra):
                return await interaction.response.send_message(
                    f"Seuls les membres de la <@&{ID_ROLE_GARDE}> peuvent posséder une spécialité double.",
                    ephemeral=True
                )

            if has_cra + has_jet + has_commando == 2:
                return await interaction.response.send_message(
                    f"{member.mention} possède déjà la spécialité double.",
                    ephemeral=True
                )

            if has_garde and (has_commando or has_jet or has_cra):
                await member.add_roles(interaction.guild.get_role(ID_ROLE_DOUBLE_SPE))

            role_to_add = interaction.guild.get_role(ID_ROLE_RECRUE_JET if is_recrue_jet else ID_ROLE_RECRUE_COMMANDO)
            await member.add_roles(role_to_add)
            await member.add_roles(interaction.guild.get_role(ID_ROLE_SPECIALITE))

            embed_validation = discord.Embed(title="Candidature spécialité acceptée",
                                             description=f"> {member.mention}, vous avez été __**accepté**__ pour devenir : \n> **{recrue.value}**\n",
                                             color=discord.Color.green())
            embed_validation.add_field(name="🪖 Formation", value="> Vous devrez passer une formation avant de pouvoir l'utiliser sur le champ de bataille, les annonces formation sont annoncées ici : <#1329545998262865940>.", inline=True)
            embed_validation.set_footer(text=f"Acceptée par {interaction.user}",
                                        icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(f"{member.mention}", embed=embed_validation)

            channel = self.bot.get_channel(ID_LOGS)
            return await channel.send(f"{member.mention} a été accepté pour devenir :\n__**{recrue.value}**__\n")


        else:
            raison_embed = "  •  Raison : " + raison if raison else ""
            embed_refus = discord.Embed(title="Candidature spécialité refusée",
                                             description=f"Soldat {member.mention}, votre candidature a été __**refusée**__.\n",
                                             color=discord.Color.red())
            embed_refus.set_footer(text=f"Refusée par {interaction.user}{raison_embed}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(f"{member.mention}", embed=embed_refus)
