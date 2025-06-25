import discord
import json
import os
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from USEFUL_IDS import ID_LOGS, ID_LOGS_HAUT_STAFF

REPORTS_FILE = "reports.json"

class ReportCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="report",
        description="Report un joueur sur son comportement anonymement même pour le staff."
    )
    @app_commands.describe(
        membre="Le membre à report",
        raison="La raison de ton report",
        anonyme="Souhaites-tu que ce soit anonyme ?"
    )
    @app_commands.choices(anonyme=[
        app_commands.Choice(name="👤 Anonyme", value="true"),
        app_commands.Choice(name="🙎 Pas anonyme", value="false")
    ])
    async def report(
        self,
        interaction: discord.Interaction,
        membre: discord.Member,
        raison: str,
        anonyme: str = "true"
    ):
        cache_bool = anonyme == "true"

        try:
            if interaction.guild is None:
                return await interaction.response.send_message("Vous ne pouvez pas utiliser cette commande en message privé.", ephemeral=True)

            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y à %H:%M:%S")

            report_data = {
                "date": timestamp,
                "reporteur_id": interaction.user.id,
                "reporteur_pseudo": str(interaction.user),
                "membre_id": membre.id,
                "membre_pseudo": str(membre),
                "raison": raison
            }

            if not os.path.exists(REPORTS_FILE):
                with open(REPORTS_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

            with open(REPORTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            data.append(report_data)

            with open(REPORTS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            footer = f"Reporté le {timestamp}"

            embed_anonyme = discord.Embed(title="🚨 Nouveau report", color=discord.Color.red())
            embed_anonyme.add_field(name="Membre signalé", value=f"{membre.mention} (`{membre}`)", inline=False)
            embed_anonyme.add_field(name="Raison", value=raison, inline=False)
            embed_anonyme.set_footer(text=footer)
            ##############################################
            embed_non_anonyme = discord.Embed(title="🚨 Nouveau report", color=discord.Color.dark_red())
            embed_non_anonyme.set_author(name=f"Report par : {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            embed_non_anonyme.add_field(name="Reporteur", value=interaction.user.mention, inline=False)
            embed_non_anonyme.add_field(name="Membre signalé", value=f"{membre.mention} (`{membre}`)", inline=False)
            embed_non_anonyme.add_field(name="Raison", value=raison, inline=False)
            embed_non_anonyme.set_footer(text=footer)

            log_channel = self.bot.get_channel(ID_LOGS)
            log_channel_high_staff = self.bot.get_channel(ID_LOGS_HAUT_STAFF)

            if log_channel and log_channel_high_staff:
                if cache_bool:
                    await log_channel_high_staff.send(embed=embed_non_anonyme)
                    await log_channel.send(embed=embed_anonyme)
                else:
                    await log_channel.send(embed=embed_non_anonyme)

            confirmation = "Le report a bien été envoyé anonymement. ✅" if cache_bool else "Le report a bien été envoyé. ✅"
            await interaction.response.send_message(confirmation, ephemeral=True)

        except Exception as e:
            print(f"Erreur lors du report : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue lors du report, veuillez contacter Wivex pour lui signaler le bug.",
                ephemeral=True
            )
