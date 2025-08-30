import discord
from discord.ext import commands
from discord import app_commands
from USEFUL_IDS import (
    ID_ROLE_LANCEUR,
    ID_LANCEMENT_SESSION,
    ID_ANNONCE_SESSION,
    REGIMENTS_LIST_NAME,
    GRADE_ORDER,
    CHECK_GREEN_REACT,
    LATE_REACT,
    RED_CROSS_REACT,
    IDK_REACT
)


def get_highest_grade_index(member: discord.Member):
    role_names = [r.name.lower() for r in member.roles]
    for i, grade in enumerate(GRADE_ORDER):
        if grade.lower() in role_names:
            return i
    return len(GRADE_ORDER)


def is_cadet(member: discord.Member):
    return any(role.name.lower() == "cadet clone trooper" for role in member.roles)


class ConfirmationView(discord.ui.View):
    def __init__(self, embed, description):
        super().__init__(timeout=None)
        self.embed = embed
        self.description = description

    @discord.ui.button(label="✅ Envoyer les escouades dans #➪📋lancement-sessions", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        salon = interaction.guild.get_channel(ID_LANCEMENT_SESSION)
        await salon.send(embed=self.embed)
        await interaction.response.edit_message(content="✅ Message envoyé avec succès.", embed=None, view=None)

    @discord.ui.button(label="❌ Annuler l'envoie", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Envoi annulé.", embed=None, view=None)


@app_commands.context_menu(name="Créer les escouades")
async def escouade_context(interaction: discord.Interaction, message: discord.Message):

    if not any(role.id == ID_ROLE_LANCEUR for role in interaction.user.roles):
        await interaction.response.send_message(
            f"❌ Seuls les <@&{ID_ROLE_LANCEUR}> peuvent utiliser cette commande.",
            ephemeral=True
        )
        return

    if message.channel.id != ID_ANNONCE_SESSION:
        await interaction.response.send_message(
            f"❌ Tu dois sélectionner un message dans <#{ID_ANNONCE_SESSION}>.",
            ephemeral=True
        )
        return

    reaction_priority = {
        CHECK_GREEN_REACT: 1,
        LATE_REACT: 2,
        RED_CROSS_REACT: 3,
        IDK_REACT: 4
    }

    user_best_status = {}
    for reaction in message.reactions:
        emoji = str(reaction.emoji)
        if emoji in reaction_priority:
            async for user in reaction.users():
                if user.bot:
                    continue
                current_priority = reaction_priority[emoji]
                existing_priority = reaction_priority.get(user_best_status.get(user.id, ("", 999))[0], 999)
                if current_priority < existing_priority:
                    user_best_status[user.id] = (emoji, current_priority)

    users_status = {}
    for user_id, (emoji, _) in user_best_status.items():
        status = "on_time" if emoji == CHECK_GREEN_REACT else "late" if emoji == LATE_REACT else "ignored"
        if status in ("on_time", "late"):
            users_status[user_id] = status

    if not users_status:
        await interaction.response.send_message(
            f"❌ Aucun utilisateur trouvé avec {CHECK_GREEN_REACT} ou {LATE_REACT}.",
            ephemeral=True
        )
        return

    regiments_dict = {reg: [] for reg in REGIMENTS_LIST_NAME}
    member_status = {}
    member_to_reg = {}
    orphan_members = []

    for user_id, status in users_status.items():
        member = message.guild.get_member(user_id)
        if not member:
            continue
        member_status[member.id] = status
        found = False
        for role in member.roles:
            for reg in REGIMENTS_LIST_NAME:
                if reg.lower() in role.name.lower():
                    regiments_dict[reg].append(member)
                    member_to_reg[member.id] = reg
                    found = True
                    break
            if found:
                break
        if not found:
            member_to_reg[member.id] = None
            orphan_members.append(member)

    merged_escouades = []
    for reg, members in regiments_dict.items():
        if len(members) < 3:
            merged_escouades.extend(members)
            regiments_dict[reg] = []

    for orphan in merged_escouades + orphan_members:
        target_reg = min(
            (r for r in regiments_dict if regiments_dict[r]),
            key=lambda r: len(regiments_dict[r]),
            default=None
        )
        if target_reg:
            regiments_dict[target_reg].append(orphan)
        else:
            regiments_dict["Mixte"] = regiments_dict.get("Mixte", []) + [orphan]

    desc = ""
    squads_count = 0
    retardataires_count = sum(1 for status in member_status.values() if status == "late")

    present_emojis = [CHECK_GREEN_REACT, LATE_REACT]
    absent_emojis = [RED_CROSS_REACT, IDK_REACT]
    present_count = sum(1 for emoji, _ in user_best_status.values() if emoji in present_emojis)
    absent_count = sum(1 for emoji, _ in user_best_status.values() if emoji in absent_emojis)
    total_reacted = present_count + absent_count
    participation_rate = round((present_count / total_reacted) * 100) if total_reacted > 0 else 0

    all_used_regiments = set()

    for reg, members in regiments_dict.items():
        if not members:
            continue

        members.sort(key=get_highest_grade_index)
        regiments_in_squad = set(
            r for m in members if (r := member_to_reg.get(m.id)) and r != "Inconnu"
        )

        if not regiments_in_squad:
            squad_name = "Mixte"
        elif len(regiments_in_squad) == 1:
            squad_name = next(iter(regiments_in_squad))
        else:
            squad_name = " & ".join(sorted(regiments_in_squad))

        all_used_regiments.update(regiments_in_squad)
        squads_count += 1

        desc += f"**{squad_name}**\n"
        for m in members:
            tags = []
            if member_status.get(m.id) == "late":
                tags.append("en retard")
            if is_cadet(m):
                tags.append("cadet")
            tag_str = f" *({' / '.join(tags)})*" if tags else ""
            desc += f"• {m.mention}{tag_str}\n"
        desc += "\n"

    total = len(users_status)
    jump_url = message.jump_url
    regiments_count = len(all_used_regiments)

    description = (
            f"🔗 [**Lien vers le message de la session**]({jump_url})\n"
            f"👥 **Total de joueurs :** {total}\n"
            f"⌛ **Retardataires :** {retardataires_count}\n"
            f"🪖 **Nombre d’escouades :** {squads_count}\n"
            f"📌 **Régiments représentés :** {regiments_count}\n"
            f"📊 **Taux de participation :** {participation_rate}%\n\n"
            f"-------------------------------\n\n"
            f"{desc}"
        )

    embed = discord.Embed(
        title="📋 Répartition des escouades",
        description=description,
        color=discord.Color.blurple()
    )
    embed.set_footer(
        text=f"Escouades créées par {interaction.user.name}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(
        content=f"{description}",
        ephemeral=True,
        view=ConfirmationView(embed, description)
    )


class EscouadeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.tree.add_command(escouade_context)

    async def cog_unload(self):
        self.bot.tree.remove_command(escouade_context.name, type=escouade_context.type)
