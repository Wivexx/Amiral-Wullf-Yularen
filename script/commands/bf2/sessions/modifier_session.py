import discord
from discord import app_commands
from discord.ext import commands
import datetime
from USEFUL_IDS import ID_ROLE_REPUBLIQUE, ID_ANNONCE_SESSION, ID_ROLE_LANCEUR, CHECK_GREEN_REACT, LATE_REACT, RED_CROSS_REACT, IDK_REACT


class CommandeSessionModifier(commands.Cog):
    @app_commands.command(name="modifier-session", description="Modifie une session déjà envoyée.")
    @app_commands.describe(
        lien="Lien du message à modifier",
        lanceur="Personne qui organise la session",
        date="Date de la session (JJ/MM/AAAA)",
        heure="Heure prévue (ex: 16h..)",
        minute="Minute (ex: ..h00)",

    )
    @app_commands.choices(
        heure=[app_commands.Choice(name=heure, value=heure.replace("h..", "")) for heure in [
            "10h..", "11h..", "12h..", "13h..", "14h..", "15h..",
            "16h..", "17h..", "18h..", "19h..", "20h..", "21h.."]],
        minute=[app_commands.Choice(name=minute, value=minute.replace("..h", "")) for minute in [
            "..h00", "..h15", "..h30", "..h45"]]
    )
    async def modifier_session(
            self,
            interaction: discord.Interaction,
            lien: str,
            lanceur: discord.Member,
            date: str,
            heure: app_commands.Choice[str],
            minute: app_commands.Choice[str],
            commentaire: str = ""
    ):
        if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
            await interaction.response.send_message(
                f"❌ Vous devez être <@&{ID_ROLE_LANCEUR}> pour modifier une session.",
                ephemeral=True
            )
            return

        try:
            message_id = int(lien.split("/")[-1])
        except ValueError:
            await interaction.response.send_message("❌ Lien invalide.", ephemeral=True)
            return

        try:
            dt = datetime.datetime.strptime(f"{date} {heure.value}:{minute.value}", "%d/%m/%Y %H:%M")
            timestamp = int(dt.timestamp())
        except ValueError:
            await interaction.response.send_message("❌ Format de date invalide. JJ/MM/AAAA attendu.", ephemeral=True)
            return

        try:
            salon = interaction.guild.get_channel(ID_ANNONCE_SESSION)
            if not salon:
                await interaction.response.send_message("❌ Salon introuvable.", ephemeral=True)
                return

            message = await salon.fetch_message(message_id)
        except discord.NotFound:
            await interaction.response.send_message("❌ Message introuvable.", ephemeral=True)
            return

        if heure.value == "21" and minute.value == "45":
            minute.value = "30"

        comment = "" if not commentaire else f"💬 __**Commentaire**__\n> {commentaire}\n\n"
        embed = discord.Embed(
            title="📣 Annonce session (modifiée)",
            description=(
                f"\n🗓️ __**Date**__\n> <t:{timestamp}:F>\n\n"
                f"⏰ __**Heure**__\n> {heure.value}h{minute.value}  -  <t:{timestamp}:R>\n\n"
                f"🎯 __**Lanceur**__\n> {lanceur.mention}\n> {lanceur.name}\n\n"
                f"{comment}"
                f"-# __**Modification des réactions maximum 1h à l'avance.**__\n\n"
            ),
            color=discord.Color.orange()
        )

        embed.set_footer(text=f"Modifié par {interaction.user}", icon_url=interaction.user.display_avatar.url)
        embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.stickers.gg%2Fstickers%2F8419-clone-salute.png&f=1&nofb=1&ipt=0b40d02fd337ae2daa49cede2bc6abea714b27929a6285948b878bd7273fc443")

        if message.embeds and message.embeds[0].image and message.embeds[0].image.url:
            embed.set_image(url=message.embeds[0].image.url)

        await interaction.response.send_message(
            content=f"⚠️ Es-tu sûr de vouloir modifier ce message ? Relis bien les infos avant de valider.\n",
            embed=embed,
            ephemeral=True,
            view=ConfirmationEditView(embed, message)
        )


class ConfirmationEditView(discord.ui.View):
    def __init__(self, embed, message):
        super().__init__(timeout=60)
        self.embed = embed
        self.message = message

    @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.message.edit(content=f"<@&{ID_ROLE_REPUBLIQUE}>", embed=self.embed)
        await interaction.response.edit_message(content="✅ Le message a bien été modifié.", embed=None, view=None)

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Modification annulée.", embed=None, view=None)
