import random
import discord
from discord import app_commands
from discord.ext import commands
import datetime
from script.commands.bf2.USEFUL_IDS import (ID_ANNONCE_SESSION_FORMATION,
                                            ID_ROLE_FORMATEUR_JET, ID_ROLE_FORMATEUR_COMMANDO,
                                            CHECK_GREEN_REACT, LATE_REACT, RED_CROSS_REACT, IDK_REACT,
                                            session_forma_commando_pics, session_forma_jet_pics)


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
        recrue=[app_commands.Choice(name=recrue, value=recrue) for recrue in [
            "🛡 Recrue Jet-Trooper", "🗡 Recrue Commando-Clone"]],
        heure=[app_commands.Choice(name=heure, value=heure.replace("h..", "")) for heure in [
            "10h..", "11h..", "12h..", "13h..", "14h..", "15h..",
            "16h..", "17h..", "18h..", "19h..", "20h..", "21h..", "22h.."]],
        minute=[app_commands.Choice(name=minute, value=minute.replace("..h", "")) for minute in [
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
            await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_FORMATEUR_JET}> pour en lancer une.",
                                                    ephemeral=True)
            return

        if recrue.value == "🗡 Recrue Commando-Clone" and not any(role.id == ID_ROLE_FORMATEUR_COMMANDO for role in interaction.user.roles):
            await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_FORMATEUR_COMMANDO}> pour en lancer une.",
                                                    ephemeral=True)
            return

        MENTION_ID = 1138872599624028282 if recrue.value == "🗡 Recrue Commando-Clonene" else 1130876977792958465

        try:
            dt = datetime.datetime.strptime(f"{date} {heure.value}:{minute.value}", "%d/%m/%Y %H:%M")
            timestamp = int(dt.timestamp())
        except ValueError:
            await interaction.response.send_message("❌ Format de date invalide. Assure-toi qu'il est sous la forme JJ/MM/AAAA.", ephemeral=True)
            return

        pics: list
        if recrue.value == "🗡 Recrue Commando-Clone":
            formation_type = "Commando-Clone"
            pics = session_forma_commando_pics
        else:
            formation_type = "Jet-Trooper"
            pics = session_forma_jet_pics

        embed = discord.Embed(
            title=f"📣 Formation {formation_type}",
            color=discord.Color.blue()
        )
        comment = "" if not commentaire else f"💬 **Commentaire :** {commentaire}\n\n"
        embed.add_field(name="",
                value=(
                    f"\n🗓️ **Date :** <t:{timestamp}:D>\n\n"
                    f"⏰ **Heure :** {heure.value}h{minute.value}  -  ||<t:{timestamp}:R>||\n\n"
                    f"🎯 **Lanceur :** {lanceur.mention}\n\n"
                    f"{comment}"
                ))

        embed.set_footer(text=f"Session lancée par {interaction.user}", icon_url=interaction.user.display_avatar.url)
        embed.set_image(url=random.choice(pics))

        await interaction.response.send_message(
            content=f"⚠️ Es-tu sûr de vouloir lancer cette session ? Relis bien les infos avant de valider.\n<@&{MENTION_ID}>",
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
        await interaction.response.edit_message(content="✅ Session envoyée avec succès !", embed=None, view=None)

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="🫡 Spécialités validées",
            url="https://discord.com/channels/947567879442812928/1131276373743386624",
            style=discord.ButtonStyle.link
        ))
        view.add_item(discord.ui.Button(
            label="🔄 Spécialités refusées",
            url="https://discord.com/channels/947567879442812928/1355847090369990715",
            style=discord.ButtonStyle.link
        ))
        view.add_item(discord.ui.Button(
            label="🃏 Presets",
            url="https://discord.com/channels/947567879442812928/1145333227284856923",
            style=discord.ButtonStyle.link
        ))

        MENTION_ID = 1138872599624028282 if self.recrue_value == "🗡 Recrue Commando-Clone" else 1130876977792958465
        message = await salon.send(f"<@&{MENTION_ID}>", embed=self.embed, view=view)

        for emoji in [CHECK_GREEN_REACT, RED_CROSS_REACT, IDK_REACT, LATE_REACT]:
            await message.add_reaction(emoji)

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Envoi annulé.", embed=None, view=None)
