import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from USEFUL_IDS import (ID_ROLE_CHEF_REGIMENT, ID_ROLE_SECOND_REGIMENT, ID_ROLE_COMMANDANT_OP,
                                            REGIMENTS_LIST_NAME, ID_ROLE_REGIMENT, ID_ROLE_GARDE, ID_ROLE_ELITE)

class EjecterRegimentCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ejecter-regiment", description="Utilise cette commande pour éjecter quelqu'un de ton régiment.")
    async def ejecter_regiment(self, interaction: discord.Interaction, member: discord.Member):

        AUTHORIZED_IDS = {ID_ROLE_CHEF_REGIMENT, ID_ROLE_SECOND_REGIMENT, ID_ROLE_COMMANDANT_OP}
        user_role_ids = {role.id for role in interaction.user.roles}

        if not AUTHORIZED_IDS & user_role_ids:
            return await interaction.response.send_message(
                f"Vous devez être <@&{ID_ROLE_CHEF_REGIMENT}>, <@&{ID_ROLE_SECOND_REGIMENT}> ou <@&{ID_ROLE_COMMANDANT_OP}> pour utiliser cette commande.",
                ephemeral=True)

        if not any(ID_ROLE_REGIMENT == role.id for role in member.roles):
            return await interaction.response.send_message(
                f"{member.mention} ne fait parti d'aucun régiment.",
                ephemeral=True)

        role_to_remove = discord.Object
        for role in interaction.user.roles:
            if role.name in REGIMENTS_LIST_NAME:
                if role.id == ID_ROLE_GARDE:
                    await member.remove_roles(interaction.guild.get_role(ID_ROLE_ELITE))
                role_to_remove = interaction.guild.get_role(role.id)
                await member.remove_roles(role_to_remove)
                await member.remove_roles(interaction.guild.get_role(ID_ROLE_REGIMENT))
                break

        embed = discord.Embed(title="Éjecté du régiment",
                                         description=f"{member.mention} ne fait plus parti de {role_to_remove.mention}",
                                         color=role_to_remove.color)
        embed.set_footer(text=f"Éjecté par {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(f"{member.mention}", embed=embed)

