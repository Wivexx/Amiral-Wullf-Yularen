import discord
from discord import app_commands
from discord.ext import commands
import re


class EmojiInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="emoji-info", description="Donne des infos sur un emoji custom Discord.")
    @app_commands.describe(emoji="Emoji custom ou Unicode")
    async def emojiinfo(self, interaction: discord.Interaction, emoji: str):
        match = re.match(r"<(a?):(\w+):(\d+)>", emoji)

        if match:
            animated, name, emoji_id = match.groups()
            emoji_obj = discord.PartialEmoji(name=name, id=int(emoji_id), animated=bool(animated))

            embed = discord.Embed(title="🔍 Infos sur l'emoji custom", color=discord.Color.blurple())
            embed.add_field(name="Nom", value=name, inline=True)
            embed.add_field(name="ID", value=emoji_id, inline=True)
            embed.add_field(name="Animé", value="Oui" if animated else "Non", inline=True)
            embed.add_field(name="Type", value="Emoji custom", inline=True)
            embed.add_field(name="Lien", value=emoji_obj.url, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            codepoints = ' '.join(f"U+{ord(char):04X}" for char in emoji)
            embed = discord.Embed(title="🔍 Infos sur l'emoji Unicode", color=discord.Color.green())
            embed.add_field(name="Emoji", value=emoji, inline=True)
            embed.add_field(name="Type", value="Emoji standard (Unicode)", inline=True)
            embed.add_field(name="Codepoint", value=codepoints, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
