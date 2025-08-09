import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from USEFUL_IDS import (ID_ROLE_FORMATEUR_JET, ID_ROLE_FORMATEUR_COMMANDO,
                                            ID_ROLE_APPRENTI_FORMATEUR, ID_ROLE_INSTRUCTEUR,
                                            GRADE_ORDER, ID_ROLE_ADJUDANT,
                                            ID_LOGS)

class CandidatureFormateurCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="candidature-formateur", description="Utilise cette commande pour accepter ou refuser une candidature d'apprenti formateur.")
    @app_commands.choices(
        validation=[
        app_commands.Choice(name="✅ Candidature acceptée", value=1),
        app_commands.Choice(name="🚫 Candidature refusée", value=0)]
    )
    @app_commands.describe(raison="/!\\ Raison SI REFUS /!\\")
    async def candidature_specialite(self, interaction: discord.Interaction, member: discord.Member, validation:int, raison: str = ""):

        if not any(ID_ROLE_INSTRUCTEUR == role.id for role in interaction.user.roles):
            return await interaction.response.send_message(f"Vous devez être <@&{ID_ROLE_INSTRUCTEUR}> pour utiliser cette commande.",
                ephemeral=True)

        if validation:
            member_grades = [role.name for role in member.roles if role.name in GRADE_ORDER]

            highest_grade = sorted(member_grades, key=lambda g: GRADE_ORDER.index(g))[0]

            if GRADE_ORDER.index(highest_grade) > GRADE_ORDER.index("Adjudant"):
                return await interaction.response.send_message(
                    f"{member.mention} ne peut pas être accepté : son grade actuel est **{highest_grade}**, "
                    f"il doit être au minimum <@&{ID_ROLE_ADJUDANT}>",
                    ephemeral=True
                )


            role_to_add = interaction.guild.get_role(ID_ROLE_APPRENTI_FORMATEUR)
            await member.add_roles(role_to_add)

            embed_validation = discord.Embed(title="Candidature formateur acceptée",
                                             description=f"> {member.mention}, vous avez été __**accepté**__ pour devenir : \n> <@&{ID_ROLE_APPRENTI_FORMATEUR}>\n"
                                                         "> Mes félicitations !\n",
                                             color=discord.Color.green())
            embed_validation.add_field(name="🔗 Invitation", value=f"> D'ici peu de temps, {interaction.user.mention} devrait vous envoyer en privé l'invitation pour rejoindre le serveur tier.", inline=False)
            embed_validation.set_footer(text=f"Acceptée par {interaction.user}",
                                        icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(f"{member.mention}", embed=embed_validation)

            channel = self.bot.get_channel(ID_LOGS)
            return await channel.send(f"{member.mention} a été accepté pour devenir :\n__**{recrue.value}**__\n")


        else:
            raison_embed = "  •  Raison : " + raison if raison else ""
            embed_refus = discord.Embed(title="Candidature formateur refusée",
                                             description=f"Soldat {member.mention}, votre candidature a été __**refusée**__.\n",
                                             color=discord.Color.red())
            embed_refus.set_footer(text=f"Refusée par {interaction.user}{raison_embed}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(f"{member.mention}", embed=embed_refus)
