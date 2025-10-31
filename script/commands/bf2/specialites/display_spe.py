import discord
from discord.ext import commands
from discord import app_commands
from USEFUL_IDS import (
    REGIMENTS_LIST_NAME, ID_ROLE_JET, ID_ROLE_COMMANDO, ID_ROLE_RECRUE_JET,
    ID_ROLE_RECRUE_COMMANDO, ID_ROLE_CRA
)


class SpecialitePaginationView(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed], current_page: int = 0):
        super().__init__(timeout=180)
        self.embeds = embeds
        self.current_page = current_page
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        self.add_item(PreviousPageButton(disabled=(self.current_page == 0)))
        self.add_item(NextPageButton(disabled=(self.current_page == len(self.embeds) - 1)))
        self.add_item(PageIndicatorButton(f"{self.current_page + 1}/{len(self.embeds)}"))

    async def change_page(self, interaction: discord.Interaction, new_page: int):
        self.current_page = new_page
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)


class PreviousPageButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(label="⬅️", style=discord.ButtonStyle.grey, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        view: SpecialitePaginationView = self.view
        await view.change_page(interaction, view.current_page - 1)


class NextPageButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(label="➡️", style=discord.ButtonStyle.grey, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        view: SpecialitePaginationView = self.view
        await view.change_page(interaction, view.current_page + 1)


class PageIndicatorButton(discord.ui.Button):
    def __init__(self, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, disabled=True)


class DisplaySpecialiteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="afficher-specialite",
        description="Affiche les membres d'une spécialité."
    )
    @app_commands.choices(
        specialite=[
            app_commands.Choice(name="🛡 Jet-Trooper", value=2),
            app_commands.Choice(name="🗡 Commando Clone", value=1),
            app_commands.Choice(name="🔫 Soldat CRA", value=0)
        ],
        mention=[
            app_commands.Choice(name="🙎 Afficher avec la mention", value=1),
            app_commands.Choice(name="👤 Afficher sans la mention", value=0)
        ]
    )
    async def afficher_specialite(
        self, interaction: discord.Interaction,
        specialite: app_commands.Choice[int],
        mention: app_commands.Choice[int]
    ):
        dict_reg = {reg: [] for reg in REGIMENTS_LIST_NAME}
        dict_reg["Sans régiment"] = []

        for member in interaction.guild.members:
            reg = None
            has_specialite = False
            is_recrue = False

            for role in member.roles:
                if role.name in REGIMENTS_LIST_NAME:
                    reg = role.name

                if specialite.value == 2:
                    if role.id == ID_ROLE_JET:
                        has_specialite = True
                    elif role.id == ID_ROLE_RECRUE_JET:
                        has_specialite = True
                        is_recrue = True

                elif specialite.value == 1:
                    if role.id == ID_ROLE_COMMANDO:
                        has_specialite = True
                    elif role.id == ID_ROLE_RECRUE_COMMANDO:
                        has_specialite = True
                        is_recrue = True

                elif specialite.value == 0:
                    if role.id == ID_ROLE_CRA:
                        has_specialite = True

            if has_specialite:
                entry = (member, is_recrue)
                if reg:
                    dict_reg[reg].append(entry)
                else:
                    dict_reg["Sans régiment"].append(entry)

        for reg in dict_reg:
            dict_reg[reg].sort(key=lambda x: x[0].joined_at or discord.utils.snowflake_time(x[0].id))

        embeds = []
        page_members = []
        current_size = 0
        PAGE_LIMIT = 5000

        for regiment in REGIMENTS_LIST_NAME + ["Sans régiment"]:
            members_list = dict_reg[regiment]

            value = "\n".join(
                f"- {(m.mention if mention.value else m.display_name)}{' *`(recrue)`*' if is_recrue else ''}"
                for m, is_recrue in members_list
            ) or "Aucun membre"

            section_text = f"__**{regiment}**__\n{value}\n\n"

            if current_size + len(section_text) > PAGE_LIMIT:
                embed = discord.Embed(
                    title=f"Liste des {specialite.name}",
                    description="".join(page_members),
                    color=discord.Color.dark_blue()
                )
                embeds.append(embed)
                page_members = [section_text]
                current_size = len(section_text)
            else:
                page_members.append(section_text)
                current_size += len(section_text)

        if page_members:
            embed = discord.Embed(
                title=f"Liste des {specialite.name}",
                description="".join(page_members),
                color=discord.Color.dark_blue()
            )
            embeds.append(embed)

        if not embeds:
            embeds = [discord.Embed(
                title=f"Liste des {specialite.name}",
                description="Aucun membre trouvé.",
                color=discord.Color.red()
            )]

        if len(embeds) == 1:
            await interaction.response.send_message(embed=embeds[0], ephemeral=True)
        else:
            view = SpecialitePaginationView(embeds)
            await interaction.response.send_message(embed=embeds[0], view=view, ephemeral=True)
