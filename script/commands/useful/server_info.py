import discord
import requests
from discord.ext import commands
from discord import app_commands

class ServerInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="server-info",
                                  description="Fetches information about a Discord server using an invite URL.")
    @discord.app_commands.describe(
        invite_url="The invite URL of the Discord server (e.g. https://discord.gg/your-invite-code).")
    async def serverinfo(self, interaction: discord.Interaction, invite_url: str):

        try:
            invite_code = invite_url.split("/")[-1]

            response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")

            if response.status_code == 200:
                data = response.json()

                server_data = data.get('guild', {})

                type_value = data.get('type', 'None')
                code_value = data.get('code', 'None')
                inviter_id = data.get('inviter', {}).get('id', 'None')
                inviter_name = data.get('inviter', {}).get('username', 'None')
                inviter_avatar = data.get('inviter', {}).get('avatar', 'None')
                inviter_discriminator = data.get('inviter', {}).get('discriminator', 'None')
                expires_at = data.get('expires_at', 'None')
                server_id = server_data.get('id', 'None')
                server_name = server_data.get('name', 'None')
                server_icon = server_data.get('icon', 'None')
                server_features = server_data.get('features', [])
                server_verification_level = server_data.get('verification_level', 'None')
                server_nsfw_level = server_data.get('nsfw_level', 'None')
                server_premium_subscriptions = server_data.get('premium_subscription_count', 'None')
                server_boost_count = server_data.get('premium_subscription_count', 0)
                server_creation_date = discord.utils.snowflake_time(int(server_id)).strftime("%d %b %Y at %H:%M")

                if 1 <= server_boost_count <= 6:
                    boost_level = "(Level 1)"
                elif 7 <= server_boost_count <= 13:
                    boost_level = "(Level 2)"
                elif server_boost_count > 13:
                    boost_level = "(Level 3)"
                else:
                    boost_level = "(Level 0)"

                possible_features = [
                    "BANNER", "INVITE_SPLASH", "NEWS", "PRIVATE_THREADS", "COMMUNITY",
                    "SEVEN_DAY_THREAD_ARCHIVE", "GUILD_ONBOARDING_HAS_PROMPTS", "ROLE_ICONS",
                    "TEXT_IN_VOICE_ENABLED", "GUILD_ONBOARDING_EVER_ENABLED", "SOUNDBOARD",
                    "ANIMATED_ICON", "MEMBER_PROFILES", "AUTO_MODERATION", "CHANNEL_ICON_EMOJIS_GENERATED",
                    "GUILD_ONBOARDING", "GUILD_SERVER_GUIDE", "THREE_DAY_THREAD_ARCHIVE",
                    "WELCOME_SCREEN_ENABLED"
                ]

                features = {f: "Yes" if f in server_features else "No" for f in possible_features}
                formatted_features = "\n".join(
                    [f"- **{key.replace('_', ' ').title()}** : {value}" for key, value in features.items()])

                embed = discord.Embed(title=f"Server Information: {server_name}", color=discord.Color.dark_red())
                embed.set_thumbnail(url=f"https://cdn.discordapp.com/icons/{server_id}/{server_icon}.png")

                embed.add_field(name="Invite", value=invite_url, inline=False)
                embed.add_field(name="Invitation Type", value=type_value, inline=True)
                embed.add_field(name="Code", value=code_value, inline=True)
                embed.add_field(name="Expires At", value=expires_at, inline=True)
                embed.add_field(name="Server ID", value=server_id, inline=True)
                embed.add_field(name="Server Name", value=server_name, inline=True)
                embed.add_field(name="Server Creation Date", value=server_creation_date, inline=True)
                embed.add_field(name="Features", value=formatted_features, inline=False)
                embed.add_field(name="NSFW Level", value=server_nsfw_level, inline=True)
                embed.add_field(name="Verification Level", value=server_verification_level, inline=True)
                embed.add_field(name="Nitro boosts", value=f"{server_premium_subscriptions} {boost_level}", inline=True)

                if inviter_name != "None":
                    embed.add_field(name="Inviter Information", value=f"Name: {inviter_name}#{inviter_discriminator}\nID: {inviter_id}\nProfile Picture: [cdn.discordapp.com](https://cdn.discordapp.com/avatars/{inviter_id}/{inviter_avatar}.png)", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                await interaction.response.send_message("Error retrieving invitation information.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)
