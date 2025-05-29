import discord
from discord import app_commands
from discord.ext import commands

def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator

class ScanServerCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="scan-server",
                          description="Scans the server for role hierarchy issues and unverified bots with dangerous permissions.")
    async def scan(self, interaction: discord.Interaction):
        if not is_admin(interaction):
            return await interaction.response.send_message(
                "You do not have permission to execute this command.", ephemeral=True
            )

        server = interaction.guild
        roles_sorted = sorted(server.roles, key=lambda r: r.position, reverse=True)

        role_categories = {
            "⚫ **All Perms**": [],
            "🔴 **A Lot of Perm**": [],
            "🟠 **Some Perm**": [],
            "🟡 **Minimal Perms**": [],
            "🟢 **Member**": []
        }

        for role in roles_sorted:
            if any(member.bot and role in member.roles for member in server.members):
                continue

            perms = role.permissions
            role_mention = role.mention

            if perms.administrator:
                role_categories["⚫ **All Perms**"].append(role_mention)
            elif perms.manage_guild or perms.ban_members or perms.manage_channels or perms.manage_roles:
                role_categories["🔴 **A Lot of Perm**"].append(role_mention)
            elif perms.moderate_members or perms.kick_members:
                role_categories["🟠 **Some Perm**"].append(role_mention)
            elif perms.manage_messages or perms.mute_members or perms.deafen_members:
                role_categories["🟡 **Minimal Perms**"].append(role_mention)
            else:
                role_categories["🟢 **Member**"].append(role_mention)

        embed = discord.Embed(
            title="🔍 Server Security Scan",
            description=(
                "Scan for **role hierarchy issues** and **unverified bots with dangerous permissions**.\n"
                "**---**\n"
                "⚠️ **Note:** Only the default Discord role should be assigned to bots. "
                "Avoid giving custom roles with high permissions to ensure security."
            ),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=server.icon.url if server.icon else None)

        manager_roles = [
            r for r in roles_sorted
            if r.permissions.manage_roles and not r.permissions.administrator
               and not any(member.bot and r in member.roles for member in server.members)
        ]

        issues_found = False
        vulnerable_members = set()
        dangerous_roles = []

        for manager in manager_roles:
            for lower_role in roles_sorted:
                if any(member.bot and lower_role in member.roles for member in server.members):
                    continue

                if lower_role.position < manager.position and lower_role.permissions.administrator:
                    issues_found = True
                    dangerous_roles.append((manager, lower_role))

                    for member in server.members:
                        if manager in member.roles:
                            vulnerable_members.add(member.mention)

        if issues_found:
            actual_hierarchy = []
            dangerous_role_mentions = {role.mention for _, role in dangerous_roles}
            manager_role_mentions = {manager.mention for manager, _ in dangerous_roles}

            for index, role in enumerate(roles_sorted[:30]):
                warning = " ⚠ " if role.mention in dangerous_role_mentions or role.mention in manager_role_mentions else ""
                actual_hierarchy.append(f"{index + 1}. {role.mention}{warning}")
            if len(roles_sorted) > 30: actual_hierarchy.append("...")

            embed.add_field(
                name="\n🔹 --- **ACTUAL ROLE HIERARCHY** --- 🔹",
                value="\n".join(actual_hierarchy) if actual_hierarchy else "None",
                inline=False
            )

            embed.add_field(name="🔹 --- **RECOMMENDED HIERARCHY** --- 🔹", value="", inline=False)

            recommended_roles = {
                "⚫ **All Perms**": set(),
                "🔴 **A Lot of Perm**": set()
            }

            for manager, lower_role in dangerous_roles:
                recommended_roles["⚫ **All Perms**"].add(lower_role.mention)
                recommended_roles["🔴 **A Lot of Perm**"].add(manager.mention)

            for category in recommended_roles.keys():
                if recommended_roles[category]:
                    embed.add_field(name=category, value="\n".join(recommended_roles[category]) + "\nᅠ", inline=False)

            for category in role_categories.keys():
                if category not in ["⚫ **All Perms**", "🔴 **A Lot of Perm**"]:
                    embed.add_field(name=category, value="Keep current roles\nᅠ", inline=False)

            embed.set_footer(text="⚠️ Review your role hierarchy to ensure proper security.")
            embed.color = discord.Color.red()

            embed.add_field(name="\n🔹 ------------------------------------ 🔹", value="ᅠ", inline=True)


            manage_roles_members = set()

            for role in roles_sorted:
                if role.permissions.manage_roles and not role.permissions.administrator:
                    for member in server.members:
                        if role in member.roles and not member.bot:
                            has_higher_admin_role = any(
                                higher_role.position > role.position and higher_role.permissions.administrator
                                for higher_role in member.roles
                            )
                            if not has_higher_admin_role:
                                manage_roles_members.add(member.mention)

            if manage_roles_members:
                embed.add_field(
                    name="🚨 --- **Member(s) that could be admin** --- 🚨",
                    value="\n".join(f"- {member}" for member in manage_roles_members),
                    inline=False
                )

        dangerous_permissions = [
            "administrator",
            "manage_channels",
            "manage_roles",
            "ban_members",
            "kick_members"
        ]

        bots_found = False
        bot_id = self.bot.user.id

        for member in server.members:
            if member.bot and member.id != bot_id:
                perms = member.guild_permissions
                risky_perms = [perm for perm in dangerous_permissions if getattr(perms, perm, False)]

                if risky_perms and not member.public_flags.verified_bot:
                    bots_found = True
                    embed.add_field(
                        name=f"\n⚠️ {member.name} (Unverified Bot)",
                        value=f"**Dangerous permissions:** {', '.join(risky_perms).replace('_', ' ')}",
                        inline=False
                    )
                    embed.color = discord.Color.red()

        if not issues_found and not bots_found:
            embed.set_footer(text="✅ No critical issues detected.")
            embed.description += "\n\n✅ **No unverified bots with dangerous permissions detected!**"

        await interaction.response.send_message(embed=embed, ephemeral=True)