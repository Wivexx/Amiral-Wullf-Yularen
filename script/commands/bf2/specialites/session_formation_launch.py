import random
import discord
from discord import app_commands
from discord.ext import commands
import datetime
from USEFUL_IDS import (ID_ANNONCE_SESSION_FORMATION,
                                            ID_ROLE_FORMATEUR_JET, ID_ROLE_FORMATEUR_COMMANDO,
                                            ID_ROLE_RECRUE_JET, ID_ROLE_RECRUE_COMMANDO,
                                            CHECK_GREEN_REACT, LATE_REACT, RED_CROSS_REACT, IDK_REACT,
                                            session_forma_commando_pics, session_forma_jet_pics, session_forma_jet_and_commando_pics)


class CommandeSessionFormationLauncher(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="session-formation", description="Lance une session de formation.")
    @app_commands.describe(
        recrue="Le type de recrue pour laquelle lancer la session",
        lanceur="Personne qui organise la session",
        date="Date de la session (JJ/MM/AAAA)",
        heure="Heure prévue (ex: 20h..)",
        minute="Minute (ex: ..h00)"
    )
    @app_commands.choices(
        recrue=[app_commands.Choice(name=r, value=r) for r in [
            "🛡 Recrue Jet-Trooper", "🗡 Recrue Commando-Clone", "🦾 Les deux"]],
        heure=[app_commands.Choice(name=h, value=h.replace("h..", "")) for h in [
            "10h..", "11h..", "12h..", "13h..", "14h..", "15h..", "16h..", "17h..", "18h.."]],
        minute=[app_commands.Choice(name=m, value=m.replace("..h", "")) for m in [
            "..h00", "..h15", "..h30", "..h45"]]
    )
    async def session(
        self,
        interaction: discord.Interaction,
        recrue: app_commands.Choice[str],
        lanceur: discord.Member,
        date: str,
        heure: app_commands.Choice[str],
        minute: app_commands.Choice[str],
        commentaire: str = ""
    ):
        if recrue.value == "🛡 Recrue Jet-Trooper" and not any(role.id == ID_ROLE_FORMATEUR_JET for role in interaction.user.roles):
            return await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_FORMATEUR_JET}> pour en lancer une.", ephemeral=True)

        if recrue.value == "🗡 Recrue Commando-Clone" and not any(role.id == ID_ROLE_FORMATEUR_COMMANDO for role in interaction.user.roles):
            return await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_FORMATEUR_COMMANDO}> pour en lancer une.", ephemeral=True)

        if recrue.value == "🦾 Les deux" and not (
            any(role.id == ID_ROLE_FORMATEUR_COMMANDO for role in interaction.user.roles)
            and any(role.id == ID_ROLE_FORMATEUR_JET for role in interaction.user.roles)):
            return await interaction.response.send_message(
                f"❌ Vous devez être <@&{ID_ROLE_FORMATEUR_COMMANDO}> __et__ <@&{ID_ROLE_FORMATEUR_JET}> pour en lancer une.",
                ephemeral=True
            )

        if recrue.value == "🗡 Recrue Commando-Clone":
            MENTION = f"<@&{ID_ROLE_RECRUE_COMMANDO}>"
        elif recrue.value == "🛡 Recrue Jet-Trooper":
            MENTION = f"<@&{ID_ROLE_RECRUE_JET}>"
        else:
            MENTION = f"<@&{ID_ROLE_RECRUE_JET}>\n<@&{ID_ROLE_RECRUE_COMMANDO}>"

        try:
            dt = datetime.datetime.strptime(f"{date} {heure.value}:{minute.value}", "%d/%m/%Y %H:%M")
            timestamp = int(dt.timestamp())
        except ValueError:
            return await interaction.response.send_message("❌ Format de date invalide. Utilise JJ/MM/AAAA.", ephemeral=True)

        if recrue.value == "🗡 Recrue Commando-Clone":
            formation_type = "Commando-Clone"
            pics = session_forma_commando_pics
        elif recrue.value == "🛡 Recrue Jet-Trooper":
            formation_type = "Jet-Trooper"
            pics = session_forma_jet_pics
        else:
            formation_type = "Jet-Trooper et Commando-Clone"
            pics = session_forma_jet_and_commando_pics

        embed = discord.Embed(title=f"📣 Formation {formation_type}", color=discord.Color.blue())
        comment = f"💬 **Commentaire :** {commentaire}\n\n" if commentaire else ""
        embed.add_field(
            name="",
            value=(
                f"🗓️ **Date :** <t:{timestamp}:D>\n\n"
                f"⏰ **Heure :** {heure.value}h{minute.value}  -  <t:{timestamp}:R>\n\n"
                f"🎯 **Lanceur :** {lanceur.mention}\n\n"
                f"{comment}"
                f"-# __**Modification des réactions maximum 1h à l'avance.**__\n\n"
            )
        )
        embed.set_footer(text=f"Session lancée par {interaction.user}", icon_url=interaction.user.display_avatar.url)
        embed.set_image(url=random.choice(pics))

        await interaction.response.send_message(
            content=f"⚠️ Es-tu sûr de vouloir lancer cette session ? Relis bien les infos avant de valider.\n{MENTION}",
            embed=embed,
            ephemeral=True,
            view=ConfirmationView(self.bot, embed, recrue.value)
        )

class ConfirmationView(discord.ui.View):
    def __init__(self, bot, embed, recrue_value: str):
        super().__init__(timeout=60)
        self.bot = bot
        self.embed = embed
        self.recrue_value = recrue_value

    @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        salon = interaction.guild.get_channel(ID_ANNONCE_SESSION_FORMATION)
        if not salon:
            return await interaction.response.send_message("❌ Salon introuvable.", ephemeral=True)

        await interaction.response.edit_message(content="✅ Session envoyée avec succès !", embed=None, view=None)

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="➪🫡 Statut Spécialités", url="https://discord.com/channels/947567879442812928/1131276373743386624"))
        view.add_item(discord.ui.Button(label="🃏 Presets", url="https://discord.com/channels/947567879442812928/1145333227284856923"))

        if self.recrue_value == "🗡 Recrue Commando-Clone":
            mention = f"<@&{ID_ROLE_RECRUE_COMMANDO}>"
        elif self.recrue_value == "🛡 Recrue Jet-Trooper":
            mention = f"<@&{ID_ROLE_RECRUE_JET}>"
        else:
            mention = f"<@&{ID_ROLE_RECRUE_JET}>\n<@&{ID_ROLE_RECRUE_COMMANDO}>"

        message = await salon.send(content=mention, embed=self.embed, view=view)

        for emoji in [CHECK_GREEN_REACT, RED_CROSS_REACT, IDK_REACT, LATE_REACT]:
            await message.add_reaction(emoji)

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Envoi annulé.", embed=None, view=None)
