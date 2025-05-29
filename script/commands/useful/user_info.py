import discord
from discord import app_commands
from discord.ext import commands
import base64

class UserInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="user-info", description="Get information about a Discord user by ID.")
    @app_commands.describe(user_id="The user id to fetch information of.")
    async def userinfo(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))

            flags = user.public_flags
            badges = []
            if flags.staff: badges.append("Discord Staff")
            if flags.partner: badges.append("Partner")
            if flags.hypesquad: badges.append("HypeSquad Member")
            if flags.bug_hunter: badges.append("Bug Hunter")
            if flags.bug_hunter_level_2: badges.append("Bug Hunter (Level 2)")
            if flags.verified_bot: badges.append("Verified Bot")
            if flags.verified_bot_developer: badges.append("Verified Developer")
            if flags.hypesquad_balance: badges.append("HypeSquad Balance")
            if flags.hypesquad_bravery: badges.append("HypeSquad Bravery")
            if flags.hypesquad_brilliance: badges.append("HypeSquad Brilliance")
            if flags.active_developer: badges.append("Active Developer")
            if flags.spammer: badges.append("Spammer")
            if flags.system: badges.append("System")
            if flags.bot_http_interactions: badges.append("HTTP Interactions")
            if flags.discord_certified_moderator: badges.append("Certified Moderator")
            if flags.early_supporter: badges.append("Early Supporter")
            if flags.early_verified_bot_developer: badges.append("Early Verified Bot Developer")
            if flags.team_user: badges.append("Team User")

            if not badges:
                badges.append("No badges")

            OnePartToken = str(base64.b64encode(str(user_id).encode("utf-8")), "utf-8").replace("=", "")
            OnePartTokenTheRealLol = "```" + OnePartToken + "...``` "

            timestamp = int(user.created_at.timestamp())

            banner_url = user.banner.url if user.banner else None

            embed = discord.Embed(
                title=f"",
                color=discord.Color.dark_red(),
            )
            embed.add_field(name="Full Name", value=f"```{user.name}#{user.discriminator}```", inline=False)
            embed.add_field(name="Display Name", value=f"```{user.display_name}```", inline=False)
            embed.add_field(name="ID", value=f"```{user.id}```", inline=False)
            embed.add_field(name="One part token", value=f"{OnePartTokenTheRealLol}", inline=False)
            embed.add_field(name="Bot?", value="Yes" if user.bot else "No", inline=False)
            embed.add_field(name="Badges", value="\n".join(f"`{badge}`" for badge in badges), inline=False)
            embed.add_field(name="Account Created On", value=f"<t:{timestamp}:R>", inline=False)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)

            if banner_url:
                embed.set_image(url=banner_url)

            creator = "** --> my creator (-Ô.Ô)  👑**" if str(user_id) == "1125789469191188550" else ""

            await interaction.response.send_message(f"<@{user_id}>" + creator, embed=embed, ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message("User not found. Please verify the ID.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message(f"An error occurred", ephemeral=True)
        except Exception:
            await interaction.response.send_message(f"Unexpected error", ephemeral=True)
