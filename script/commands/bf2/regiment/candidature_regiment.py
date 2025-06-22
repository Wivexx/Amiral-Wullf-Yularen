import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from script.commands.bf2.USEFUL_IDS import ID_ROLE_CHEF_REGIMENT, ID_ROLE_SECOND_REGIMENT, ID_ROLE_COMMANDANT_OP, REGIMENTS_LIST_NAME, ID_ROLE_REGIMENT

class CandidatureRegimentCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="candidature-regiment", description="Utilise cette commande pour accepter ou refuser une candidature pour ton régiment.")
    @app_commands.choices(validation=[
        app_commands.Choice(name="✅ Candidature acceptée", value=1),
        app_commands.Choice(name="🚫 Candidature refusée", value=0)
    ])
    @app_commands.describe(raison="/!\\ Raison SI REFUS /!\\")
    async def candidature_regiment(self, interaction: discord.Interaction, member: discord.Member, validation:int, raison: str = ""):

        AUTHORIZED_IDS = {ID_ROLE_CHEF_REGIMENT, ID_ROLE_SECOND_REGIMENT, ID_ROLE_COMMANDANT_OP}
        user_role_ids = {role.id for role in interaction.user.roles}

        if not AUTHORIZED_IDS & user_role_ids:
            return await interaction.response.send_message(
                f"Vous devez être <@&{ID_ROLE_CHEF_REGIMENT}>, <@&{ID_ROLE_SECOND_REGIMENT}> ou <@&{ID_ROLE_COMMANDANT_OP}> pour utiliser cette commande.",
                ephemeral=True)

        if validation:
            role_to_add = discord.Object
            for role in interaction.user.roles:
                if role.name in REGIMENTS_LIST_NAME:
                    role_to_add = interaction.guild.get_role(role.id)
                    await member.add_roles(role_to_add)
                    await member.add_roles(interaction.guild.get_role(ID_ROLE_REGIMENT))
                    break

            embed_validation = discord.Embed(title="Candidature régiment acceptée",
                                             description=f"Soldat {member.mention}, vous avez été __**accepté**__ dans le régiment : **{role_to_add.mention}**\n"
                                                         "Mes félicitations !\n",
                                             color=discord.Color.green())
            embed_validation.add_field(name="🔗 Invitation", value=f"D'ici peu de temps, {interaction.user.mention} devrait vous envoyer en privé l'invitation pour rejoindre le serveur du régiment.")
            embed_validation.set_footer(text=f"Acceptée par {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(f"{member.mention}", embed=embed_validation)

        else:
            raison_embed = "  •  Raison : " + raison if raison else ""
            embed_refus = discord.Embed(title="Candidature régiment refusée",
                                             description=f"Soldat {member.mention}, votre candidature a été __**refusée**__.\n",
                                             color=discord.Color.red())
            embed_refus.set_footer(text=f"Refusée par {interaction.user}{raison_embed}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(f"{member.mention}", embed=embed_refus)
