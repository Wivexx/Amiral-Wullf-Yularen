import discord
from discord.ext import commands
from discord import app_commands
from USEFUL_IDS import ID_LOGS

class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bannir un membre du serveur.")
    @app_commands.describe(member="Membre à bannir", raison="Raison du bannissement")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, raison: str = "Aucune raison fournie."):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("🚫 Vous n'avez pas la permission de bannir des membres.", ephemeral=True)
            return

        if interaction.user.top_role <= member.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("🚫 Vous ne pouvez pas bannir ce membre.", ephemeral=True)
            return

        try:
            await member.ban(reason=raison)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Impossible de bannir ce membre. Vérifiez mes permissions.", ephemeral=True)
            return

        await interaction.response.send_message(f"✅ <@{member.id}> a été banni pour : **{raison}**.", ephemeral=True)

        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name=f"{member.name} a été banni", value=f"**Raison :** {raison}\n**Par :** <@{interaction.user.id}>", inline=False)

        log_channel = self.bot.get_channel(ID_LOGS)
        if log_channel:
            await log_channel.send(embed=embed)
