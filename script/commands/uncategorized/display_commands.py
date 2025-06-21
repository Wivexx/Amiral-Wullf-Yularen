import discord
from discord.ext import commands
from script.commands.bf2.USEFUL_IDS import (ID_ROLE_STAFF, ID_ROLE_LANCEUR, ID_ROLE_FORMATEUR_COMMANDO, ID_ROLE_FORMATEUR_JET,
                                            ID_ROLE_CHEF_REGIMENT,
                                            ID_ROLE_SECOND_REGIMENT,
                                            ID_ROLE_COMMANDANT_OP
                                            )


class DisplayCommandsView(discord.ui.View):
    def __init__(self, is_staff: bool, is_lanceur: bool, is_formateur: bool, is_reg_high_perm: bool, active_page: str = "default"):
        super().__init__(timeout=None)

        self.active_page = active_page
        self.is_staff = is_staff
        self.is_lanceur = is_lanceur
        self.is_formateur = is_formateur
        self.is_reg_high_perm = is_reg_high_perm

        self.add_item(DefaultButton(disabled=(active_page == "default")))
        if is_lanceur:
            self.add_item(SessionButton(disabled=(active_page == "session")))
        if is_staff:
            self.add_item(StaffButton(disabled=(active_page == "staff")))
        if is_formateur:
            self.add_item(FormateurButton(disabled=(active_page == "formateur")))
        if is_reg_high_perm:
            self.add_item(RegimentButton(disabled=(active_page == "regiment")))

class DefaultButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(
            label="📋 Commandes générales",
            style=discord.ButtonStyle.red,
            custom_id="default_commands",
            disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.dark_red())

        embed.add_field(name="**┏—————— Non-categorisé ——————┓**",
                        value="`/display-commands`\n"
                              "`/ping`\n"
                              "`/say`\n"
                              "`/report`\n"
                              "`/serveur-stats`",
                        inline=False)

        embed.add_field(name="**┏—————— Jeux ——————┓**",
                        value="`/tirage`\n"
                              "`/biscuit-chinois`\n"
                              "`/pile-ou-face`\n"
                              "`/calculateur-amour`\n"
                              "`/boule-magique`\n"
                              "`/nombre-aleatoire`\n"
                              "`/pierre-papier-ciseaux`\n"
                              "`/morpion`\n",
                        inline=False)

        embed.add_field(name="**┏—————— Utiles ——————┓**",
                        value="`/password-check`\n"
                              "`/password-generator`\n"
                              "`/server-info`\n"
                              "`/role-info`\n"
                              "`/timestamp`\n"
                              "`/user-info`\n"
                              "`/webhook-info`\n"
                              "`/membre-info`",
                        inline=False)

        embed.set_footer(text="Total commandes: 21")

        user_roles_ids = [role.id for role in interaction.user.roles]
        is_staff = ID_ROLE_STAFF in user_roles_ids
        is_lanceur = ID_ROLE_LANCEUR in user_roles_ids
        is_formateur = ID_ROLE_FORMATEUR_COMMANDO in user_roles_ids or ID_ROLE_FORMATEUR_JET in user_roles_ids
        is_reg_high_perm = ID_ROLE_CHEF_REGIMENT in user_roles_ids or ID_ROLE_SECOND_REGIMENT in user_roles_ids or ID_ROLE_COMMANDANT_OP

        view = DisplayCommandsView(is_staff, is_lanceur, is_formateur, is_reg_high_perm, active_page="default")
        await interaction.response.edit_message(embed=embed, view=view)


class SessionButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(
            label="👥 Commandes lanceur de session",
            style=discord.ButtonStyle.green,
            custom_id="session_commands",
            disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="",
            color=discord.Color.dark_green()
        )
        embed.add_field(name="Commandes :", value=
            "`/session`\n"
            "`/escouade`\n"
            "`/modifier-session`\n"
            "`/give-role`\n"
            "`/remove-role`\n",
            inline=False
        )

        embed.set_footer(text="Total commandes: 5")

        user_roles_ids = [role.id for role in interaction.user.roles]
        is_staff = ID_ROLE_STAFF in user_roles_ids
        is_lanceur = ID_ROLE_LANCEUR in user_roles_ids
        is_formateur = ID_ROLE_FORMATEUR_COMMANDO in user_roles_ids or ID_ROLE_FORMATEUR_JET in user_roles_ids
        is_reg_high_perm = ID_ROLE_CHEF_REGIMENT in user_roles_ids or ID_ROLE_SECOND_REGIMENT in user_roles_ids or ID_ROLE_COMMANDANT_OP

        view = DisplayCommandsView(is_staff, is_lanceur, is_formateur, is_reg_high_perm, active_page="session")
        await interaction.response.edit_message(embed=embed, view=view)


class StaffButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(
            label="🛠 Commandes du staff",
            style=discord.ButtonStyle.blurple,
            custom_id="staff_commands",
            disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="",
            color=discord.Color.blurple()
        )
        embed.add_field(name="**┏—————— Haut Staff ——————┓**",
                        value="`/setup-log`\n"
                              "`/scan-server`\n",
                        inline=False
                        )
        embed.add_field(name="**┏—————— Modérateur sécurité ——————┓**",
                        value="`/ban`\n"
                              "`/kick`\n",
                        inline=False
                        )
        embed.add_field(name="**┏—————— Staff ——————┓**",
                        value="`/blackliste`\n"
                              "`/clear`\n",
                        inline=False
        )
        embed.set_footer(text="Total commandes: 6")

        user_roles_ids = [role.id for role in interaction.user.roles]
        is_staff = ID_ROLE_STAFF in user_roles_ids
        is_lanceur = ID_ROLE_LANCEUR in user_roles_ids
        is_formateur = ID_ROLE_FORMATEUR_COMMANDO in user_roles_ids or ID_ROLE_FORMATEUR_JET in user_roles_ids
        is_reg_high_perm = ID_ROLE_CHEF_REGIMENT in user_roles_ids or ID_ROLE_SECOND_REGIMENT in user_roles_ids or ID_ROLE_COMMANDANT_OP

        view = DisplayCommandsView(is_staff, is_lanceur, is_formateur, is_reg_high_perm, active_page="staff")
        await interaction.response.edit_message(embed=embed, view=view)

class FormateurButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(
            label="🪖 Commandes formateurs",
            style=discord.ButtonStyle.green,
            custom_id="formateurs_commands",
            disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="",
            color=discord.Color.green()
        )
        embed.add_field(name="Commandes :", value=
            "`/session-formation`\n"
            "`/candidature-specialite`\n",
            inline=False
        )

        embed.set_footer(text="Total commandes: 2")

        user_roles_ids = [role.id for role in interaction.user.roles]
        is_staff = ID_ROLE_STAFF in user_roles_ids
        is_lanceur = ID_ROLE_LANCEUR in user_roles_ids
        is_formateur = ID_ROLE_FORMATEUR_COMMANDO in user_roles_ids or ID_ROLE_FORMATEUR_JET in user_roles_ids
        is_reg_high_perm = ID_ROLE_CHEF_REGIMENT in user_roles_ids or ID_ROLE_SECOND_REGIMENT in user_roles_ids or ID_ROLE_COMMANDANT_OP

        view = DisplayCommandsView(is_staff, is_lanceur, is_formateur, is_reg_high_perm, active_page="formateur")
        await interaction.response.edit_message(embed=embed, view=view)


class RegimentButton(discord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(
            label="🧌 Commandes chefs de regiment",
            style=discord.ButtonStyle.grey,
            custom_id="reg_commands",
            disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="",
            color=discord.Color.light_grey()
        )
        embed.add_field(name="Commandes :", value=
            "`/candidature-regiment`\n",
            inline=False
        )

        embed.set_footer(text="Total commandes: 1")

        user_roles_ids = [role.id for role in interaction.user.roles]
        is_staff = ID_ROLE_STAFF in user_roles_ids
        is_lanceur = ID_ROLE_LANCEUR in user_roles_ids
        is_formateur = ID_ROLE_FORMATEUR_COMMANDO in user_roles_ids or ID_ROLE_FORMATEUR_JET in user_roles_ids
        is_reg_high_perm = ID_ROLE_CHEF_REGIMENT in user_roles_ids or ID_ROLE_SECOND_REGIMENT in user_roles_ids or ID_ROLE_COMMANDANT_OP

        view = DisplayCommandsView(is_staff, is_lanceur, is_formateur, is_reg_high_perm, active_page="regiment")
        await interaction.response.edit_message(embed=embed, view=view)


class DisplayCommandsCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="display-commands", description="Affiche les commandes disponibles.")
    async def display_commands(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.dark_red())

        embed.add_field(name="**┏—————— Non-categorisé ——————┓**",
                        value="`/display-commands`\n"
                              "`/ping`\n"
                              "`/say`\n"
                              "`/report`\n"
                              "`/serveur-stats`",
                        inline=False)

        embed.add_field(name="**┏—————— Jeux ——————┓**",
                        value="`/tirage`\n"
                              "`/biscuit-chinois`\n"
                              "`/pile-ou-face`\n"
                              "`/calculateur-amour`\n"
                              "`/boule-magique`\n"
                              "`/nombre-aleatoire`\n"
                              "`/pierre-papier-ciseaux`\n"
                              "`/morpion`\n",
                        inline=False)

        embed.add_field(name="**┏—————— Utiles ——————┓**",
                        value="`/password-check`\n"
                              "`/password-generator`\n"
                              "`/server-info`\n"
                              "`/role-info`\n"
                              "`/timestamp`\n"
                              "`/user-info`\n"
                              "`/webhook-info`\n"
                              "`/membre-info`",
                        inline=False)

        embed.set_footer(text="Total commandes: 21")

        user_roles_ids = [role.id for role in interaction.user.roles]
        is_staff = ID_ROLE_STAFF in user_roles_ids
        is_lanceur = ID_ROLE_LANCEUR in user_roles_ids
        is_formateur = ID_ROLE_FORMATEUR_COMMANDO in user_roles_ids or ID_ROLE_FORMATEUR_JET in user_roles_ids
        is_reg_high_perm = ID_ROLE_CHEF_REGIMENT in user_roles_ids or ID_ROLE_SECOND_REGIMENT in user_roles_ids or ID_ROLE_COMMANDANT_OP

        if is_staff or is_lanceur or is_formateur:
            view = DisplayCommandsView(is_staff, is_lanceur, is_formateur, is_reg_high_perm, active_page="default")
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else: await interaction.response.send_message(embed=embed, ephemeral=True)
