import discord
import json
import os
from discord.ext import commands

CONFIG_FILE = "log_channel_ids.json"

class ClearCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="clear", description="Supprime un nombre spécifié de messages dans le canal.")
    @discord.app_commands.describe(amount="Nombre de messages à supprimer.")
    async def clear(self, interaction: discord.Interaction, amount: int = 5):
        try:
            if interaction.guild is None:
                return await interaction.response.send_message("Vous ne pouvez pas utiliser cette commande dans un message privé.", ephemeral=True)

            if not interaction.user.guild_permissions.manage_messages:
                return await interaction.response.send_message("Seuls les modérateurs peuvent utiliser cette commande.", ephemeral=True)

            if amount > 100:
                return await interaction.response.send_message("Le nombre maximum de messages pouvant être supprimés est de 100.", ephemeral=True)

            if not isinstance(interaction.channel, discord.TextChannel):
                return await interaction.response.send_message("Vous devez exécuter cette commande dans un canal textuel.", ephemeral=True)

            if amount <= 0:
                return await interaction.response.send_message("Vous devez choisir un nombre supérieur à 0.", ephemeral=True)

            guild_id = str(interaction.guild.id)
            log_channel_id = None

            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as file:
                    config_data = json.load(file)
                    log_channel_id = config_data.get(guild_id)

            if not log_channel_id:
                return await interaction.response.send_message(
                    "Aucun salon de log n'est configuré pour ce serveur. Veuillez utiliser la commande `/setuplog`.", ephemeral=True)

            CHANNEL_LOG = self.bot.get_channel(int(log_channel_id))

            if not CHANNEL_LOG:
                return await interaction.response.send_message(f"Le salon de log ({log_channel_id}) configuré est introuvable. Veuillez vérifier l'ID.", ephemeral=True)

            await interaction.response.send_message(f"{amount}x {'message supprimé' if amount == 1 else 'messages supprimés'} ! 👍", ephemeral=True)

            await interaction.channel.purge(limit=amount)

            embed = discord.Embed(color=discord.Color.dark_red())
            embed.add_field(
                name=f"{amount}x {message_type} dans: <#{interaction.channel.id}>",
                value=f"\n\n**Commande utilisée par :** <@{interaction.user.id}>",
                inline=False)

            await CHANNEL_LOG.send(embed=embed)

        except Exception:
            await interaction.response.send_message(
                f"Une erreur s'est produite : {e}\n"
                f"Veuillez configurer le canal de journalisation avec `/setup-log [ID du canal]` avant de supprimer des messages.",
                ephemeral=True)
