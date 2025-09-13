import discord
from discord.ext import commands
from discord import app_commands
from USEFUL_IDS import ID_ROLE_REPUBLIQUE, ID_ROLE_STAFF

class CounterCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="counter-activite", description="Affiche le nombre de message envoyé par les membres VS le staff")
    async def counter_activite(self, interaction: discord.Interaction):
        try:
            from script.events.events import load_counter

            counter = load_counter()

            republic_role = interaction.guild.get_role(ID_ROLE_REPUBLIQUE)
            staff_role = interaction.guild.get_role(ID_ROLE_STAFF)

            republic_members = len(republic_role.members)
            staff_members = len(staff_role.members)

            republic_msgs = counter["counter"]["republic"]
            staff_msgs = counter["counter"]["staff"]

            avg_republic = republic_msgs / republic_members if republic_members > 0 else 0
            avg_staff = staff_msgs / staff_members if staff_members > 0 else 0

            total_avg = avg_republic + avg_staff
            republic_pct = (avg_republic / total_avg * 100) if total_avg > 0 else 0
            staff_pct = (avg_staff / total_avg * 100) if total_avg > 0 else 0

            embed = discord.Embed(color=discord.Color.dark_magenta())
            embed.add_field(name="📈 __Counter activité infos__", value="", inline=False)

            embed.add_field(
                name="République :",
                value=(
                    f"💬 Messages totaux : `{republic_msgs}`\n"
                    f"👥 Membres : `{republic_members}`\n"
                    f"📊 Pourcentage pondéré : `{republic_pct:.2f}%`"
                ), inline=True)

            embed.add_field(
                name="Staff :",
                value=(
                    f"💬 Messages totaux : `{staff_msgs}`\n"
                    f"👥 Membres : `{staff_members}`\n"
                    f"📊 Pourcentage pondéré : `{staff_pct:.2f}%`"
                ), inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"Erreur dans /counter : {e}")
