import random

import discord
from discord import app_commands
from discord.ext import commands
import datetime
from script.commands.bf2.USEFUL_IDS import ID_ROLE_REPUBLIQUE, ID_ANNONCE_SESSION, ID_ROLE_LANCEUR, CHECK_GREEN_REACT, LATE_REACT, RED_CROSS_REACT, IDK_REACT


class CommandeSessionLauncher(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="session", description="Lance une session.")
    @app_commands.describe(
        lanceur="Personne qui organise la session",
        date="Date de la session (JJ/MM/AAAA)",
        heure="Heure prévue (ex: 20h..)",
        minute="Minute (ex: ..h00)"
    )
    @app_commands.choices(
        heure=[app_commands.Choice(name=heure, value=heure.replace("h..", "")) for heure in [
            "10h..", "11h..", "12h..", "13h..", "14h..", "15h..",
            "16h..", "17h..", "18h..", "19h..", "20h..", "21h..", "22h.."]],
        minute=[app_commands.Choice(name=minute, value=minute.replace("..h", "")) for minute in [
            "..h00", "..h15", "..h30", "..h45"]]
    )
    async def session(
        self,
        interaction: discord.Interaction,
        lanceur: discord.Member,
        date: str,
        heure: app_commands.Choice[str],
        minute: app_commands.Choice[str],
        commentaire: str = ""
    ):
        if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
            await interaction.response.send_message(f"❌ Vous devez être <@&{ID_ROLE_LANCEUR}> pour en lancer une.", ephemeral=True)
            return

        try:
            dt = datetime.datetime.strptime(f"{date} {heure.value}:{minute.value}", "%d/%m/%Y %H:%M")
            timestamp = int(dt.timestamp())
        except ValueError:
            await interaction.response.send_message("❌ Format de date invalide. Assure-toi qu'il est sous la forme JJ/MM/AAAA.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📣 Annonce session",
            description=(
                f"\n🗓️ **Date :** <t:{timestamp}:D>\n\n"
                f"⏰ **Heure :** {heure.value}h{minute.value}  -  ||<t:{timestamp}:R>||\n\n"
                f"🎯 **Lanceur :** {lanceur.mention}\n\n"
            ),
            color=discord.Color.dark_blue()
        )
        if commentaire:
            embed.add_field(name="", value=f"💬 **Commentaire :** {commentaire}\n\n")

        embed.set_footer(text=f"Session lancée par {interaction.user}", icon_url=interaction.user.display_avatar.url)
        session_pics = [
            "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.EYnEMKDumO_MzcqSicvv7gHaDt%26pid%3DApi&f=1&ipt=6985444a0cf7c83e83c8b051c7e843f2dc8f6a19b0abc7739ca2c2ec24428c91&ipo=images",
            "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.gjmozccI4rSTnt3GRfOd9QHaEK%26pid%3DApi&f=1&ipt=c4b96d57a0ca49e2dfb050f9847758c92e21c1d5499ac241496acf9d21ed4517&ipo=images",
            "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.XtXlNCZ5Ao6jpXIvo33PDAHaEK%26pid%3DApi&f=1&ipt=c2782efe38919d9e0090ae7bb14cfa6f3bd92aaa8ecfa10da5c3eee6e597ccc6&ipo=images",
            "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.explicit.bing.net%2Fth%3Fid%3DOIP.Dnp2-Gex2LcaQosdbqKLmQHaDt%26pid%3DApi&f=1&ipt=d7c3689de14ea7540e19f17c060c90bd999c2f5a9195887df0764d21cd07ad43&ipo=images",
            "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.yzKbQbDV5aXuQwTWN0HKmwHaEK%26pid%3DApi&f=1&ipt=122ea1110b58d2758210667f5c82b0c233f6576948ffad0c3dfb5fd5e7e485d4&ipo=images",
            "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.R7QYN-TV52MeZ_yQw3NNogHaEK%26pid%3DApi&f=1&ipt=46181f99f47209cfe65c5a02f6a754a0a898c07b9dcc409fcd7b56e706379765&ipo=images"]
        embed.set_image(url=random.choice(session_pics))

        await interaction.response.send_message(
            content=f"⚠️ Es-tu sûr de vouloir lancer cette session ? Relis bien les infos avant de valider.\n<@&{ID_ROLE_REPUBLIQUE}>",
            embed=embed,
            ephemeral=True,
            view=ConfirmationView(self.bot, embed)
        )

class ConfirmationView(discord.ui.View):
    def __init__(self, bot, embed):
        super().__init__(timeout=60)
        self.bot = bot
        self.embed = embed

    @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        salon = interaction.guild.get_channel(ID_ANNONCE_SESSION)
        await interaction.response.edit_message(content="✅ Session envoyée avec succès !", embed=None, view=None)

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="📲 À ajouter",
            url="https://discord.com/channels/947567879442812928/1231619386649870336",
            style=discord.ButtonStyle.link
        ))
        view.add_item(discord.ui.Button(
            label="🃏 Presets",
            url="https://discord.com/channels/947567879442812928/1145333227284856923",
            style=discord.ButtonStyle.link
        ))
        view.add_item(discord.ui.Button(
            label="🗯 Langage RP",
            url="https://discord.com/channels/947567879442812928/1211384057334730752",
            style=discord.ButtonStyle.link
        ))
        view.add_item(discord.ui.Button(
            label="📈 Compte de session",
            url="https://discord.com/channels/947567879442812928/1066110693109158008",
            style=discord.ButtonStyle.link
        ))

        message = await salon.send(f"<@&{ID_ROLE_REPUBLIQUE}>", embed=self.embed, view=view)

        for emoji in [CHECK_GREEN_REACT, RED_CROSS_REACT, IDK_REACT, LATE_REACT]:
            await message.add_reaction(emoji)

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Envoi annulé.", embed=None, view=None)
