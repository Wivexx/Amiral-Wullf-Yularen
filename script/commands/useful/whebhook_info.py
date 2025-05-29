import discord
from discord.ext import commands
from discord import app_commands
import requests

class WebhookInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="webhook-info", description="Lookup information for a webhook URL.")
    @app_commands.describe(webhook_url="The webhook url like https://discord.com/api/webhooks/...")
    async def webhook_info(self, interaction: discord.Interaction, webhook_url: str):
        INFO_ADD = "[+]"
        COLOR_RED_DARK = discord.Color.dark_red()

        if not webhook_url:
            embed = discord.Embed(
                title="Webhook Info",
                description="Command Usage:",
                color=COLOR_RED_DARK
            )
            embed.add_field(
                name="Syntax:",
                value="`/webhook-info [webhook_url]`",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.get(webhook_url, headers=headers)

            if response.status_code != 200:
                await interaction.response.send_message("Error: Invalid or inaccessible webhook.", ephemeral=True)
                return

            webhook_info = response.json()
            embed = discord.Embed(
                title="Webhook Information",
                color=COLOR_RED_DARK
            )
            embed.add_field(name=f"{INFO_ADD} ID", value=webhook_info.get('id', "None"), inline=False)
            embed.add_field(name=f"{INFO_ADD} Token", value=webhook_info.get('token', "None"), inline=False)
            embed.add_field(name=f"{INFO_ADD} Name", value=webhook_info.get('name', "None"), inline=False)
            embed.add_field(name=f"{INFO_ADD} Avatar", value=webhook_info.get('avatar', "None"), inline=False)
            embed.add_field(
                name=f"{INFO_ADD} Type",
                value="Bot" if webhook_info.get('type') == 1 else "User",
                inline=False
            )
            embed.add_field(name=f"{INFO_ADD} Channel ID", value=webhook_info.get('channel_id', "None"), inline=False)
            embed.add_field(name=f"{INFO_ADD} Server ID", value=webhook_info.get('guild_id', "None"), inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

            if 'user' in webhook_info:
                user_info = webhook_info['user']
                user_embed = discord.Embed(
                    title="Associated User Information",
                    color=COLOR_RED_DARK
                )
                user_embed.add_field(name=f"{INFO_ADD} ID", value=user_info.get('id', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Name", value=user_info.get('username', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Display Name", value=user_info.get('global_name', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Discriminator", value=user_info.get('discriminator', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Avatar", value=user_info.get('avatar', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Flags", value=user_info.get('flags', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Accent Color", value=user_info.get('accent_color', "None"), inline=False)
                user_embed.add_field(name=f"{INFO_ADD} Banner Color", value=user_info.get('banner_color', "None"), inline=False)

                await interaction.followup.send(embed=user_embed, ephemeral=True)

        except Exception as e:
            error_embed = discord.Embed(
                title="Error During the Request",
                description=str(e),
                color=COLOR_RED_DARK
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)