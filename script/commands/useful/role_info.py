import discord
from discord import app_commands
from discord.ext import commands

class RoleInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="role-info", description="Get information about a specific role.")
    @app_commands.describe(role="The role to fetch information of.")
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):

        embed = discord.Embed(color=role.color, title="Role Information")
        embed.add_field(name="Role Name", value=f"<@&{role.id}>", inline=True)
        embed.add_field(name="Role ID", value=str(role.id), inline=True)
        embed.add_field(name="Users in Role", value=str(len(role.members)), inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Displayed Separately", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Permissions", value=("\n".join([f"`{perm[0]}`" for perm in role.permissions if perm[1]]) if role.permissions else "None") if not role.permissions.administrator else "`All perms`", inline=False)
        embed.add_field(name="Position", value=str(role.position), inline=True)
        embed.add_field(name="Default Role", value="Yes" if role.is_default() else "No", inline=True)
        embed.add_field(name="Mentioned by @everyone", value="Yes" if role.mentionable else "No", inline=True)
        embed.set_footer(text=f"Role created on {role.created_at.strftime('%d %b %Y at %H:%M')}")

        await interaction.response.send_message(embed=embed, ephemeral=True)
