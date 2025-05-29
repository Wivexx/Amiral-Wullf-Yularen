import discord
from discord.ext import commands
from discord.ui import View, Button

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

BOT_OWNER_ID = 1125789469191188550


class ConfirmationView(View):
    def __init__(self, ctx, guild):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.guild = guild

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(
            title="⏳ Timed Out",
            description="You took too long to respond. The operation has been canceled.",
            color=discord.Color.red()
        )
        await self.ctx.send(embed=embed, view=self)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != BOT_OWNER_ID:
            return await interaction.response.send_message("❌ You are not allowed to use this button!", ephemeral=True)

        embed = discord.Embed(
            title="✅ Bot Left Server",
            description=f"The bot has successfully left `{self.guild.name}`.",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=None)
        await self.guild.leave()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != BOT_OWNER_ID:
            return await interaction.response.send_message("❌ You are not allowed to use this button!", ephemeral=True)

        embed = discord.Embed(
            title="❌ Command Canceled",
            description="The bot will not leave the server.",
            color=discord.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=None)


def LeaveCommand(bot: commands.Bot):
    @bot.command(name="leave", aliases=["lvr", "exit", "ext"])
    async def leave_server(ctx, *, server_id: int = None):

        if ctx.author.id != BOT_OWNER_ID:
            return

        try:
            guild = bot.get_guild(server_id) if server_id else ctx.guild

            if not guild:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No server found with this ID.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title="⚠️ Leave Server Confirmation",
                description=f"The bot is about to leave `{guild.name}` (ID: `{guild.id}`).\n"
                            f"Please confirm by clicking one of the buttons below.",
                color=discord.Color.orange()
            )
            embed.set_footer(text="You have 30 seconds to respond.")

            view = ConfirmationView(ctx, guild)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            embed = discord.Embed(
                title="❌ An Error Occurred",
                description=f"```{e}```",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
