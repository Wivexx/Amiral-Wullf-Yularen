import discord
from discord.ext import commands
from discord import app_commands

from USEFUL_IDS import (
    ID_SESSION_PLAYER,
    ID_ANNONCE_SESSION,
    ID_ROLE_LANCEUR,
    ID_ESCOUADE_HEAD,
    CHECK_GREEN_REACT,
    LATE_REACT
)


class ChefSelectView(discord.ui.View):
    def __init__(self, members, role_player, role_head):
        super().__init__(timeout=180)
        self.role_player = role_player
        self.role_head = role_head
        self.members = members

        self.select = discord.ui.UserSelect(
            placeholder="Sélectionne les chefs d’escouade",
            min_values=1,
            max_values=25
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        chefs = self.select.values
        count_player, count_head = 0, 0
        failed_players, failed_heads = [], []

        for member in self.members:
            try:
                await member.add_roles(self.role_player)
                count_player += 1
            except Exception:
                failed_players.append(member.display_name)

        for member in chefs:
            try:
                await member.add_roles(self.role_head)
                count_head += 1
            except Exception:
                failed_heads.append(member.display_name)

        desc = (
            f"→ <@&{self.role_player.id}> ajouté à **{count_player}** joueur(s)\n"
            f"→ <@&{self.role_head.id}> ajouté à **{count_head}** chef(s)"
        )
        if failed_players:
            desc += f"\n⚠ Erreurs (joueurs) : {' - '.join(failed_players)}"
        if failed_heads:
            desc += f"\n⚠ Erreurs (chefs) : {' - '.join(failed_heads)}"

        embed = discord.Embed(
            title="🟢 Attribution des rôles terminée",
            description=desc,
            color=discord.Color.green()
        )
        await interaction.edit_original_response(content="", embed=embed, view=None)


@app_commands.context_menu(name="Donner les rôles de session")
async def give_role_context(interaction: discord.Interaction, message: discord.Message):

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

    member_ids = set()
    for reaction in message.reactions:
        if str(reaction.emoji) in [CHECK_GREEN_REACT, LATE_REACT]:
            async for user in reaction.users():
                if not user.bot:
                    member = interaction.guild.get_member(user.id)
                    if member:
                        member_ids.add(member.id)

    members = [interaction.guild.get_member(uid) for uid in member_ids]
    if not members:
        await interaction.response.send_message("❌ Aucun joueur trouvé avec les réactions.", ephemeral=True)
        return

    role_player = interaction.guild.get_role(ID_SESSION_PLAYER)
    role_head = interaction.guild.get_role(ID_ESCOUADE_HEAD)

    view = ChefSelectView(members, role_player, role_head)
    await interaction.response.send_message(
        content="👉 Sélectionne les chefs d’escouades dans le menu ci-dessous :",
        ephemeral=True,
        view=view
    )


class CommandeGiveRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.tree.add_command(give_role_context)

    async def cog_unload(self):
        self.bot.tree.remove_command(give_role_context.name, type=give_role_context.type)
