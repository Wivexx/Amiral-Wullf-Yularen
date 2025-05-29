import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from script.commands.bf2.USEFUL_IDS import (
    ID_ROLE_REPUBLIQUE, ID_ROLE_STAFF, ID_ROLE_CANDA, ID_ROLE_ORAL,
    REGIMENTS_LIST_NAME, GRADE_ORDER
)

class ServeurStatsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MembresButton())
        self.add_item(RolesButton())
        self.add_item(InfosButton())

class MembresButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📊 Membres", style=discord.ButtonStyle.green, custom_id="membres_stats")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        total = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        online = len([m for m in guild.members if not m.bot and m.status != discord.Status.offline])

        def get_role_data(role_id):
            role = guild.get_role(role_id)
            if role:
                count = len(role.members)
                return count, round((count / total) * 100, 2)
            return 0, 0.0

        rep, rep_pct = get_role_data(ID_ROLE_REPUBLIQUE)
        staff, staff_pct = get_role_data(ID_ROLE_STAFF)
        canda, canda_pct = get_role_data(ID_ROLE_CANDA)
        oral, oral_pct = get_role_data(ID_ROLE_ORAL)

        embed = discord.Embed(title="📊 Statistiques Membres", color=discord.Color.green())
        embed.add_field(name="Général",
                        value=f"👥 Total : {total}\n🟢 En ligne : {online}\n🤖 Bots : {bots}", inline=False)
        embed.add_field(name="Rôles spécifiques",
                        value=f"🛡 République : {rep} ({rep_pct}%)\n"
                              f"🧰 Staff : {staff} ({staff_pct}%)\n"
                              f"📋 Canda à faire : {canda} ({canda_pct}%)\n"
                              f"🎤 Oral à faire : {oral} ({oral_pct}%)", inline=False)
        await interaction.response.edit_message(embed=embed, view=ServeurStatsView())

class RolesButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🎖 Rôles", style=discord.ButtonStyle.blurple, custom_id="roles_stats")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        regiment_stats = ""
        for r in REGIMENTS_LIST_NAME:
            role = discord.utils.get(guild.roles, name=r)
            if role:
                regiment_stats += f"- **{r}** : {len(role.members)}\n"

        grade_stats = ""
        for grade in GRADE_ORDER:
            role = discord.utils.get(guild.roles, name=grade)
            if role:
                grade_stats += f"- **{grade}** : {len(role.members)}\n"

        embed = discord.Embed(title="🎖 Statistiques Rôles", color=discord.Color.blurple())
        embed.add_field(name="Par Régiment", value=regiment_stats or "Aucun", inline=False)
        embed.add_field(name="Par Grade", value=grade_stats or "Aucun", inline=False)
        await interaction.response.edit_message(embed=embed, view=ServeurStatsView())

class InfosButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🧾 Infos générales", style=discord.ButtonStyle.red, custom_id="info_stats")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        created_at = discord.utils.format_dt(guild.created_at, "D")
        owner = guild.owner.mention if guild.owner else "Inconnu"
        roles = len(guild.roles)
        boosts = guild.premium_subscription_count
        level = guild.premium_tier
        vocaux = len(guild.voice_channels)
        textuels = len(guild.text_channels)
        total = vocaux + textuels
        in_vocal = sum(len(vc.members) for vc in guild.voice_channels)

        embed = discord.Embed(title="🧾 Informations Générales", color=discord.Color.red())
        embed.add_field(name="Création", value=f"📅 {created_at}", inline=False)
        embed.add_field(name="Créateur", value=f"👑 {owner}", inline=False)
        embed.add_field(name="Rôles", value=f"🏷 {roles} rôles", inline=False)
        embed.add_field(name="Canaux", value=f"💬 Textuels : {textuels}\n🔊 Vocaux : {vocaux}\n📦 Total : {total}", inline=False)
        embed.add_field(name="En vocal", value=f"🎙 Membres en vocal : {in_vocal}", inline=False)
        embed.add_field(name="Boosts", value=f"🚀 Niveau {level} avec {boosts} boosts", inline=False)
        await interaction.response.edit_message(embed=embed, view=ServeurStatsView())

class CommandeServeurStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="serveur-stats", description="Affiche les statistiques du serveur.")
    async def serveur_stats(self, interaction: discord.Interaction):
        guild = interaction.guild
        total = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        online = len([m for m in guild.members if not m.bot and m.status != discord.Status.offline])

        def get_role_data(role_id):
            role = guild.get_role(role_id)
            if role:
                count = len(role.members)
                return count, round((count / total) * 100, 2)
            return 0, 0.0

        rep, rep_pct = get_role_data(ID_ROLE_REPUBLIQUE)
        staff, staff_pct = get_role_data(ID_ROLE_STAFF)
        canda, canda_pct = get_role_data(ID_ROLE_CANDA)
        oral, oral_pct = get_role_data(ID_ROLE_ORAL)

        embed = discord.Embed(title="📊 Statistiques Membres", color=discord.Color.green())
        embed.add_field(name="Général",
                        value=f"👥 Total : {total}\n🟢 En ligne : {online}\n🤖 Bots : {bots}", inline=False)
        embed.add_field(name="Rôles spécifiques",
                        value=f"🛡 République : {rep} ({rep_pct}%)\n"
                              f"🧰 Staff : {staff} ({staff_pct}%)\n"
                              f"📋 Canda à faire : {canda} ({canda_pct}%)\n"
                              f"🎤 Oral à faire : {oral} ({oral_pct}%)", inline=False)

        await interaction.response.send_message(embed=embed, view=ServeurStatsView(), ephemeral=True)