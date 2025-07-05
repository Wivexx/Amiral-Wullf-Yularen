import discord
from discord import app_commands
from discord.ext import commands
import datetime
import json
import os

BIRTHDAYS_FILE = "birthdays.json"

def load_birthdays():
    if not os.path.exists(BIRTHDAYS_FILE):
        return {}
    with open(BIRTHDAYS_FILE, "r") as f:
        return json.load(f)

def save_birthdays(data):
    with open(BIRTHDAYS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class AddBirthdayModal(discord.ui.Modal, title="🎉 Ajouter / Modifier ton anniversaire"):
    def __init__(self, user: discord.User, existing_data=None):
        self.user = user
        placeholder_date = "01/01"
        placeholder_year = "2004"
        placeholder_ping = "oui"

        if existing_data:
            placeholder_date = f"{existing_data['day']:02d}/{existing_data['month']:02d}"
            if existing_data.get("with_year") and existing_data.get("year"):
                placeholder_year = str(existing_data["year"])
            placeholder_ping = "oui" if existing_data.get("ping") else "non"

        super().__init__()
        self.date = discord.ui.TextInput(
            label="Date (JJ/MM)",
            placeholder=placeholder_date,
            required=True
        )
        self.year = discord.ui.TextInput(
            label="Année (optionnelle)",
            placeholder=placeholder_year,
            required=False
        )
        self.ping = discord.ui.TextInput(
            label="Souhaites-tu être ping ? (oui/non)",
            placeholder=placeholder_ping,
            required=True
        )
        self.add_item(self.date)
        self.add_item(self.year)
        self.add_item(self.ping)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            day, month = map(int, self.date.value.split("/"))
            datetime.datetime(day=day, month=month, year=2000)

            year_value = self.year.value.strip()
            if year_value:
                year = int(year_value)
                datetime.datetime(day=day, month=month, year=year)
                with_year = True
            else:
                year = None
                with_year = False

            ping_value = self.ping.value.strip().lower()
            ping = ping_value in ["oui", "yes", "true"]

            data = load_birthdays()
            data[str(self.user.id)] = {
                "day": day,
                "month": month,
                "year": year,
                "ping": ping,
                "with_year": with_year
            }
            save_birthdays(data)

            await interaction.response.send_message("✅ Ton anniversaire a bien été enregistré !", ephemeral=True)

        except Exception:
            await interaction.response.send_message("❌ Format invalide. Utilise JJ/MM pour la date et AAAA pour l’année.", ephemeral=True)


class AddButton(discord.ui.Button):
    def __init__(self, user, disabled):
        super().__init__(label="➕ Ajouter", style=discord.ButtonStyle.green, disabled=disabled)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddBirthdayModal(self.user))

class ModifyButton(discord.ui.Button):
    def __init__(self, user, disabled):
        super().__init__(label="⚙️ Modifier", style=discord.ButtonStyle.blurple, disabled=disabled)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        data = load_birthdays()
        existing_data = data.get(str(self.user.id))
        await interaction.response.send_modal(AddBirthdayModal(self.user, existing_data=existing_data))


class DeleteButton(discord.ui.Button):
    def __init__(self, user, disabled):
        super().__init__(label="➖ Supprimer", style=discord.ButtonStyle.red, disabled=disabled)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        data = load_birthdays()
        user_id = str(self.user.id)
        if user_id in data:
            del data[user_id]
            save_birthdays(data)
            await interaction.response.send_message("🗑️ Ton anniversaire a été supprimé.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Tu n'avais pas encore enregistré d'anniversaire.", ephemeral=True)


class ManageBirthdayButtons(discord.ui.View):
    def __init__(self, user: discord.User, exists: bool):
        super().__init__(timeout=60)
        self.add_item(AddButton(user, disabled=exists))
        self.add_item(ModifyButton(user, disabled=not exists))
        self.add_item(DeleteButton(user, disabled=not exists))


class CommandeBirthday(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="anniversaire", description="Gérer ton anniversaire")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="⚙️ Gérer mon anniversaire", value=1),
            app_commands.Choice(name="📆 Voir les 10 prochains anniversaires", value=2)
        ]
    )
    async def anniversaire(self, interaction: discord.Interaction, option: app_commands.Choice[int]):
        if option.value == 1:
            data = load_birthdays()
            user_id = str(interaction.user.id)
            exists = user_id in data

            view = ManageBirthdayButtons(interaction.user, exists)
            await interaction.response.send_message(
                "🎂 Choisis ce que tu veux faire avec ton anniversaire :",
                view=view,
                ephemeral=True)


        elif option.value == 2:

            data = load_birthdays()
            today = datetime.date.today()
            upcoming = []

            for user_id, info in data.items():
                try:
                    bday = datetime.date(today.year, info["month"], info["day"])
                    if bday < today:
                        bday = datetime.date(today.year + 1, info["month"], info["day"])
                    upcoming.append((user_id, bday))
                except Exception:
                    continue

            if not upcoming:
                await interaction.response.send_message("Aucun anniversaire enregistré.", ephemeral=True)
                return

            upcoming.sort(key=lambda x: x[1])
            upcoming = upcoming[:10]

            embed = discord.Embed(
                title="🎉 Prochains anniversaires",
                color=discord.Color.gold())

            for uid, bday in upcoming:
                try:
                    user = await self.bot.fetch_user(int(uid))
                    mention = user.mention
                    name = user.name
                except Exception as e:
                    print(f"[ERREUR] fetch_user pour {uid} : {e}")
                    mention = f"<@{uid}>"
                    name = f"Utilisateur inconnu"

                embed.add_field(name=f"{name}", value=f"{bday.strftime('%d/%m')} – {mention}", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
