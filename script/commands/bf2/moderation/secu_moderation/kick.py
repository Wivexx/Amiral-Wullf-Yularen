import discord
from discord.ext import commands
from discord import app_commands
from script.commands.bf2.USEFUL_IDS import ID_LOGS


class KickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulser un membre du serveur.")
    @app_commands.describe(member="Membre à expulser", raison="Raison de l'expulsion")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, raison: str = "Aucune raison fournie."):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("🚫 Seuls les modérateurs peuvent utiliser cette commande.", ephemeral=True)
            return

        if interaction.user.top_role <= member.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("🚫 Vous ne pouvez pas expulser ce membre.", ephemeral=True)
            return

        try:
            await member.kick(reason=raison)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Impossible d’expulser ce membre. Vérifiez mes permissions.", ephemeral=True)
            return

        await interaction.response.send_message(f"✅ <@{member.id}> a été expulsé pour : **{raison}**.", ephemeral=True)

        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name=f"{member.name} a été expulsé", value=f"**Raison :** {raison}\n**Par :** <@{interaction.user.id}>", inline=False)

        log_channel = self.bot.get_channel(ID_LOGS)
        if log_channel:
            await log_channel.send(embed=embed)
