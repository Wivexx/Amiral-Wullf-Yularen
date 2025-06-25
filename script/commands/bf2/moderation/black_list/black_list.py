import discord
from discord.ext import commands
from discord import app_commands
from USEFUL_IDS import ID_ROLE_STAFF, ID_LOGS
import os

current_dir = os.path.dirname(__file__)
BLACKLIST_FILE = os.path.join(current_dir, "blacklist.txt")

def read_blacklist():
    black_list_members = []
    try:
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as file:
            for line in file.readlines():
                if line.strip():
                    pseudo, user_id = line.strip().split(";")
                    black_list_members.append((pseudo, int(user_id)))
    except FileNotFoundError:
        print(f"Le fichier {BLACKLIST_FILE} est introuvable.")
    return black_list_members


def write_blacklist(black_list_members):
    try:
        with open(BLACKLIST_FILE, "w", encoding="utf-8") as file:
            for pseudo, user_id in black_list_members:
                file.write(f"{pseudo};{user_id}\n")
    except IOError:
        print(f"Erreur lors de l'écriture dans le fichier {BLACKLIST_FILE}.")

class BlacklistCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="blackliste", description="Gère la blackliste (staff uniquement)")
    @app_commands.describe(
        membre="Membre concerné"
    )
    @app_commands.choices(
        option=[
            app_commands.Choice(name="👀 Afficher la black-list", value=""),
            app_commands.Choice(name="➕ Ajouter un membre", value="add"),
            app_commands.Choice(name="➖ Retirer un membre", value="remove")
        ],
    )
    async def blackliste(
        self,
        interaction: discord.Interaction,
        option: str,
        membre: discord.Member = None
    ):
        black_list_members = read_blacklist()
        channel_log = self.bot.get_channel(ID_LOGS)

        if not any(role.id == ID_ROLE_STAFF for role in interaction.user.roles):
            await interaction.response.send_message(
                "**Cette commande est uniquement disponible pour le staff.**\n"
                "Si vous avez des questions, notre [support](https://discord.com/channels/947567879442812928/1062710795638677525/1295722507361321014) est à votre disposition.",
                ephemeral=True
            )
            return

        if option.lower() == "add" and membre:
            if any(user_id == membre.id for _, user_id in black_list_members):
                embed = discord.Embed(color=discord.Color.dark_red())
                embed.add_field(name=f"||{membre.name}|| est déjà dans la blacklist.", value="", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            black_list_members.append((membre.name, membre.id))
            write_blacklist(black_list_members)

            embed = discord.Embed(color=discord.Color.dark_green())
            embed.add_field(name=f"||{membre.name}|| a été ajouté à la blackliste.", value="", inline=False)
            embed.add_field(name="\n", value=f"**Par:** <@{interaction.user.id}>", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
            await channel_log.send(embed=embed)
            return

        if option.lower() == "remove" and membre:
            if any(user_id == membre.id for _, user_id in black_list_members):
                black_list_members = [entry for entry in black_list_members if entry[1] != membre.id]
                write_blacklist(black_list_members)

                embed = discord.Embed(color=discord.Color.dark_red())
                embed.add_field(name=f"||{membre.name}|| a été retiré de la blackliste.", value="", inline=False)
                embed.add_field(name="\n", value=f"**Par:** <@{interaction.user.id}>", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
                await channel_log.send(embed=embed)
            else:
                embed = discord.Embed(color=discord.Color.dark_red())
                embed.add_field(name=f"||{membre.name}|| n'est pas dans la blackliste.", value="", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if option == "":
            if len(black_list_members) == 0:
                embed = discord.Embed(
                    title="Aucun membre black-listé !",
                    color=discord.Color.dark_red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            description = "\n".join([f"- <@{user_id}>" for _, user_id in black_list_members])
            embed = discord.Embed(
                title="Liste des membres **black-listés** :",
                description="||" + description + "||",
                color=discord.Color.dark_embed()
            )
            embed.set_footer(text=f"Total des membres : {len(black_list_members)}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
