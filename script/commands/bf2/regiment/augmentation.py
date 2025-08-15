import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from USEFUL_IDS import (ID_ROLE_CHEF_REGIMENT, ID_ROLE_SECOND_REGIMENT, ID_ROLE_COMMANDANT_OP,
                        REGIMENTS_LIST_NAME, ID_ROLE_REGIMENT,
                        ID_ROLE_GARDE, ID_ROLE_ELITE, GRADE_ORDER)

class AugmentationCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="augmentation",
                          description="Utilise cette commande pour augmenter un homme de ton régiment.")
    async def augmentation(self, interaction: discord.Interaction, member: discord.Member):

        AUTHORIZED_IDS = {ID_ROLE_CHEF_REGIMENT, ID_ROLE_SECOND_REGIMENT, ID_ROLE_COMMANDANT_OP}
        user_role_ids = {role.id for role in interaction.user.roles}

        if not AUTHORIZED_IDS & user_role_ids:
            return await interaction.response.send_message(
                f"Vous devez être <@&{ID_ROLE_CHEF_REGIMENT}>, <@&{ID_ROLE_SECOND_REGIMENT}> ou <@&{ID_ROLE_COMMANDANT_OP}> pour utiliser cette commande.",
                ephemeral=True
            )

        if interaction.user.id != 123:
            return await interaction.response.send_message("# <:Developer:1380971617563316385> En construction...",
                                                           ephemeral=True)

        current_grade = None
        for role in member.roles:
            if role.name in GRADE_ORDER:
                current_grade = role.name
                break

        if not current_grade:
            return await interaction.response.send_message("❌ Ce membre n'a pas de grade valide.", ephemeral=True)

        current_index = GRADE_ORDER.index(current_grade)
        if current_index == 0:
            return await interaction.response.send_message("❌ Ce membre est déjà au grade le plus haut.",
                                                           ephemeral=True)

        new_grade_name = GRADE_ORDER[current_index - 1]
        new_grade_role = discord.utils.get(interaction.guild.roles, name=new_grade_name)

        if not new_grade_role:
            return await interaction.response.send_message(f"❌ Le rôle `{new_grade_name}` est introuvable.",
                                                           ephemeral=True)

        await member.remove_roles(discord.utils.get(interaction.guild.roles, name=current_grade))
        await member.add_roles(new_grade_role)

        embed = discord.Embed(
            title="🎖️ Augmentation",
            description=f"{member.mention} a été promu au grade **{new_grade_name}**",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Augmenté par {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)
