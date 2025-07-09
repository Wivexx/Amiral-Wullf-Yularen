from discord.enums import AppCommandOptionType
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands
from USEFUL_IDS import ID_WIVEX
import nacl

class WivexCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="wivex", description="Cette commande est réservée à Wivex.")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="🔊 Connecter le bot à un salon vocal", value=1),
            app_commands.Choice(name="🔈 Déconnecter le bot d'un salon vocal", value=2),
            app_commands.Choice(name="Envoyer embed n°1", value=3)
        ]
    )
    @app_commands.describe(option="Choisir une option")
    async def wivex(self, interaction: discord.Interaction, option: discord.app_commands.Choice[int]):

        if interaction.user.id != ID_WIVEX:
            return await interaction.response.send_message(f"Cette commande est uniquement réservée à <@{ID_WIVEX}>.", ephemeral=True)

        if option.value == 1:
            if interaction.user.voice and interaction.user.voice.channel:
                channel = interaction.user.voice.channel
                try:
                    await channel.connect()
                    await interaction.response.send_message(f"✅ Connecté à <#{channel.id}>.", ephemeral=True)
                except Exception:
                    await interaction.response.send_message(f"⚠️ Je suis déjà connecté à un salon vocal.",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Tu dois être connecté à un salon vocal pour utiliser cette commande.", ephemeral=True)

        elif option.value == 2:
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.disconnect()
                await interaction.response.send_message("👋 Déconnecté du salon vocal.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Je ne suis connecté à aucun salon vocal.", ephemeral=True)


        elif option.value == 3:
            embed = discord.Embed(color=discord.Color.pink())
            embed.add_field(name="name", value="value", inline=False)

            await interaction.response.send_message("", embed=embed, ephemeral=True)
