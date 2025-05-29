import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

class MemberInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="membre-info", description="Affiche structurellement les rôles d'un membre.")
    async def membre_info(self, interaction: discord.Interaction, member: discord.Member = None):

        member = interaction.user if member is None else member

        staff_roles = [
        "Administrateur", "Modérateur", "Helper", "Responsable Staff",
        "Modérateur Sécurité", "Modérateur Aide au Besoin", "Modérateur Communication",
        "Co-créateur||🐳", "Créateur", "Staff sieste", "BOT SUPREME", "Droïde", "Responsable technique"
    ]

        is_staff = any(role.name in staff_roles for role in member.roles)

        username = member.name
        server_user_nickname = member.nick
        global_user_name = member.global_name
        user_id = member.id
        user_avatar = member.avatar.url if member.avatar else None
        create_account = f"<t:{int(member.created_at.timestamp())}:R>"
        join_account = f"<t:{int(member.joined_at.timestamp())}:R>"

        def safe_mention(role: discord.Role):
            return f"<@&{role.id}>"


        excluded_roles = [
        "-----------type de soldat-----------", "------------grade clone-------------",
        "--------------Régiment--------------", "--------------Spécialité------------",
        "-----------Gardiens de la paix-----------",
        "-----------types de vaisseaux-----------", "---------------grade-------------- ",
        "République", "---------------grade--------------", "Staff", "Staff +", "--------------Autres--------------",
        "--------------Médaille--------------"
    ]

        platform_roles = ["PS4", "PS5"]
        session_launcher_roles = ["Lanceur de session"]

        user_roles = [role for role in member.roles if role.name != "@everyone" and role.name not in excluded_roles]

        user_staff_roles = []
        user_senat_roles = []
        type_de_soldat = []
        specialite = []
        regiment = []
        grade_clone = []
        formateur = []
        instructeur = []
        ping_roles = []
        jedi = []
        meddals = []
        booster = []
        platform = []
        session_launcher = []
        other_roles = []
        not_member_roles = []

        for role in user_roles:
            if role.name in staff_roles:
                user_staff_roles.append(safe_mention(role))
            elif role.name in ["Responsable Sénat", "Sénateur"]:
                user_senat_roles.append(safe_mention(role))
            elif role.name in ["commando", "Soldat lourd", "officier", "spécialiste"]:
                type_de_soldat.append(safe_mention(role))
            elif role.name in ["soldat cra", "Spécialité double", "commando clone", "jet trooper", "wookies",
                               "Recrue SOLDAT CRA", "Recrue COMMANDO CLONE", "Recrue JET-TROOPER",
                               "Recrue wookiee"]:
                specialite.append(safe_mention(role))
            elif role.name in ["chef de régiment", "second de régiment", "501ème Légion", "Garde de Coruscant",
                               "104ème wolfpack", "327ème corps stellaire", "212ème bataillon d'attaque",
                               "41ème corps d'élite", "Pilote de char"]:
                regiment.append(safe_mention(role))
            elif role.name in ["Colonel", "Lieutenant Colonel", "Commandant", "Capitaine", "Capitaine en second",
                               "Lieutenant", "Lieutenant en second", "Major", "Major aspirant", "Adjudant chef",
                               "Adjudant", "Sergent major", "Sergent", "Caporal-chef", "Caporal", "Clone trooper",
                               "Cadet clone trooper", "général"]:
                grade_clone.append(safe_mention(role))
            elif "ping" in role.name.lower():
                ping_roles.append(safe_mention(role))
            elif role.name in ["Maître jedi", "Chevalier jedi", "Padawan", "Initié"]:
                jedi.append(safe_mention(role))
            elif "médaille" in role.name.lower() or role.name in ["Gagnant du tournoi nº1", "Grande croix de la république", "Grand officier de la légion", "Chevalier de la légion", "Croix de la valeur"]:
                meddals.append(safe_mention(role))
            elif role.name in ["Instructeur"]:
                instructeur.append(safe_mention(role))
            elif role.name in ["Formateur Commando", "Formateur Jet-Trooper", "Apprenti formateur"]:
                formateur.append(safe_mention(role))
            elif role.name == "Les booster d'hyperdrive":
                booster.append(safe_mention(role))
            elif role.name in platform_roles:
                platform.append(safe_mention(role))
            elif role.name in session_launcher_roles:
                session_launcher.append(safe_mention(role))
            elif role.name in ["Candidature à faire", "Oral à faire"]:
                not_member_roles.append(safe_mention(role))
            else:
                other_roles.append(safe_mention(role))

        formatted_staff = " **-** ".join(user_staff_roles)
        formatted_senat = " **-** ".join(user_senat_roles) if user_senat_roles else "**Non**"
        formatted_formateur = " **-** ".join(formateur) if formateur else "**Non**"
        formatted_instructeur = "**Oui**" if instructeur else "**Non**"
        formatted_type_de_soldat = " **-** ".join(type_de_soldat) if type_de_soldat else "**Aucun**"
        formatted_specialite = " **-** ".join(specialite) if specialite else "**Aucune**"
        formatted_regiment = " **-** ".join(regiment) if regiment else "**Aucun**"
        formatted_grade_clone = " **-** ".join(grade_clone) if grade_clone else "**Aucun**"
        formatted_ping = " **-** ".join(ping_roles) if ping_roles else "**Aucun**"
        formatted_jedi = " **-** ".join(jedi) if jedi else "**Non**"
        formatted_meddal = " **-** ".join(meddals) if meddals else "**Aucune**"
        formatted_booster = " **Oui** " if booster else "**Non**"
        formatted_platform = " **-** ".join(platform) if platform else "**Aucune**"
        formatted_session_launcher = "**Oui**" if session_launcher else "**Non**"
        formatted_other_roles = " **-** ".join(other_roles) if other_roles else "**Aucun**"
        formatted_not_member = "**Non**" if not_member_roles else "**Oui**"

        if any(role.name == "général" for role in member.roles):
            grade = "Grade"
        else:
            grade = "Grade clone"

        embed_member_info = discord.Embed(color=member.top_role.color)
        embed_member_info.set_author(
            name=username,
            icon_url=member.avatar.url if member.avatar.url else None
        )
        embed_member_info.add_field(name="——————————————————————————", value="", inline=False)
        embed_member_info.add_field(name="🌍  Informations général",
                                       value=f"> `Nom du membre:` **{username}**\n"
                                             f"> `Nom global du membre:` **{global_user_name if global_user_name else username}**\n"
                                             f"> `Nom du serveur du membre:` **{server_user_nickname if server_user_nickname else username}**\n"
                                             f"> `ID du membre:` **{user_id}**\n"
                                             f"> `Avatar du membre:` **[cdn.discordapp.com]({user_avatar})**\n"
                                             f"> `Creation du compte :` **{create_account}**\n"
                                             f"> `Rejoint le serveur :` **{join_account}**"
                                             "\n",
                                       inline=False)

        if is_staff:
            embed_member_info.add_field(name="\n👑  Grade à responsabilité",
                                            value=f"> `Staff:` **Oui**\n"
                                                  f"> `Rôle staff:` {formatted_staff}\n"
                                                  f"> `Sénateur:` {formatted_senat}"
                                                  "\n",
                                            inline=False)
        else:
            embed_member_info.add_field(name="\n👑  Grade à responsabilité",
                                            value=f"> `Staff:` **Non**\n"
                                                  f"> `Sénateur:` {formatted_senat}"
                                                  "\n",
                                            inline=False)

        embed_member_info.add_field(name="\n🏹  Grade RP",
                            value=f"> `Formateur:` {formatted_formateur}\n"
                                  f"> `Instructeur:` {formatted_instructeur}\n"
                                  f"> `Type de soldat:` {formatted_type_de_soldat}\n"
                                  f"> `Spécialité:` {formatted_specialite}\n"
                                  f"> `Régiment:` {formatted_regiment}\n"
                                  f"> `{grade}:` {formatted_grade_clone}\n"
                                  f"> `Lanceur de session:` {formatted_session_launcher}\n"
                                  f"> `Jedi:` {formatted_jedi}\n"
                                  f"> `Médaille:` {formatted_meddal}"
                                  "\n",
                                  inline=False)

        embed_member_info.add_field(name="\n🎭  Grade HRP",
                            value=f"> `Booster d'hyperdrive:` {formatted_booster}\n"
                                  f"> `Platforme:` {formatted_platform}\n"
                                  f"> `Ping:` {formatted_ping}\n"
                                  f"> `Vérifié:` {formatted_not_member}\n"
                                  f"> `Autres rôles:` {formatted_other_roles}"
                                  "\n",
                            inline=False)


        button_support = Button(label="Support",
                                url="https://discord.com/channels/947567879442812928/1363479451538690260",
                                style=discord.ButtonStyle.link,
                                emoji="📞")
        button_avis = Button(label="Votre avis nous intéresse",
                             url="https://disboard.org/fr/review/create/947567879442812928",
                             style=discord.ButtonStyle.link,
                             emoji="📨")

        view = View()
        view.add_item(button_support)
        view.add_item(button_avis)

        await interaction.response.send_message(f"{member.mention}", embed=embed_member_info, view=view, ephemeral=True)