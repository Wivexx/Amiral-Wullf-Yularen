"""
Script by: wivex  (-Ò_Ó)
"""

### Import general packages
import discord
from discord.ext import commands
import asyncio

### TOKEN BOT ###
from bot_token import bot_token
from script.commands.useful.whebhook_info import WebhookInfoCommand

### Import events ###
from script.events.events import setup_events

### Import commands ###
from hidden_script.leave import LeaveCommand

from script.commands.bf2.moderation.haut_staff.scan_server import ScanServerCommand
from script.commands.bf2.moderation.haut_staff.setup_log import LogCommand

from script.commands.bf2.moderation.black_list.black_list import BlacklistCommand
from script.commands.bf2.moderation.secu_moderation.ban import BanCommand
from script.commands.bf2.moderation.clear import ClearCommand
from script.commands.bf2.moderation.secu_moderation.kick import KickCommand
from script.commands.bf2.moderation.manage_role import ManageRoleCommand

from script.commands.bf2.regiment.candidature_regiment import CandidatureRegimentCommand
from script.commands.bf2.regiment.ejecter_regiment import EjecterRegimentCommand
from script.commands.bf2.regiment.augmentation import AugmentationCommand

from script.commands.bf2.sessions.session_launch import CommandeSessionLauncher
from script.commands.bf2.sessions.modifier_session import CommandeSessionModifier
from script.commands.bf2.sessions.escouade import EscouadeCommand
from script.commands.bf2.sessions.give_role import CommandeGiveRole
from script.commands.bf2.sessions.remove_role import CommandeRemoveRole

from script.commands.bf2.specialites.candidature_formateur import CandidatureFormateurCommand
from script.commands.bf2.specialites.candidature_specialite import CandidatureSpecialiteCommand
from script.commands.bf2.specialites.session_formation_launch import CommandeSessionFormationLauncher
from script.commands.bf2.specialites.specialite_validation import SpecialiteValidationCommand

from script.commands.bf2.moderation.report import ReportCommand

from script.commands.bf2.server_stats import CommandeServeurStats
from script.commands.bf2.counter import CounterCommand

from script.commands.games.magic_ball import CommandeBouleMagique
from script.commands.games.draw import CommandeTirage
from script.commands.games.fortune_cookie import CommandeBiscuitChinois
from script.commands.games.heads_or_tails import CommandePileOuFace
from script.commands.games.random_number import CommandeNombreAleatoire
from script.commands.games.rock_paper_scissors import CommandePierrePapierCiseaux
from script.commands.games.love_calculator import CommandeCalculateurAmour
from script.commands.games.tic_tac_toe import MorpionCommande

from script.commands.useful.emoji_info import EmojiInfo
from script.commands.useful.user_info import UserInfoCommand
from script.commands.useful.password_check import PasswordCheckCommand
from script.commands.useful.server_info import ServerInfoCommand
from script.commands.useful.role_info import RoleInfoCommand
from script.commands.useful.password_generator import PasswordGeneratorCommand
from script.commands.useful.timestamp import TimestampCommand
from script.commands.useful.membre_info import MemberInfoCommand

from script.commands.useful.correction import CorrectionCommand

from script.commands.uncategorized.display_commands import DisplayCommandsCommand
from script.commands.uncategorized.say import SayCommand
from script.commands.uncategorized.ping import PingCommand
from script.commands.uncategorized.birthday import CommandeBirthday

### List of commands ###
COMMANDS = [
    ScanServerCommand,
    LogCommand,

    BanCommand,
    KickCommand,

    ClearCommand,
    BlacklistCommand,
    ManageRoleCommand,

    CandidatureRegimentCommand,
    EjecterRegimentCommand,
    AugmentationCommand,

    CommandeSessionLauncher,
    CommandeSessionModifier,
    EscouadeCommand,
    CommandeGiveRole,
    CommandeRemoveRole,

    CandidatureFormateurCommand,
    CandidatureSpecialiteCommand,
    CommandeSessionFormationLauncher,
    SpecialiteValidationCommand,

    ReportCommand,

    CommandeServeurStats,
    CounterCommand,

    CommandeBouleMagique,
    CommandeTirage,
    CommandeBiscuitChinois,
    CommandePileOuFace,
    CommandeNombreAleatoire,
    CommandePierrePapierCiseaux,
    CommandeCalculateurAmour,
    MorpionCommande,

    EmojiInfo,
    UserInfoCommand,
    PasswordCheckCommand,
    ServerInfoCommand,
    PasswordGeneratorCommand,
    TimestampCommand,
    RoleInfoCommand,
    WebhookInfoCommand,
    MemberInfoCommand,

    CorrectionCommand,

    DisplayCommandsCommand,
    SayCommand,
    PingCommand,
    CommandeBirthday,
]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

def load_hidden_commands(bot):
    LeaveCommand(bot)
    setup_events(bot)

async def stop_bot():
    await asyncio.to_thread(input, "")
    await bot.close()
    print("Bot has been stopped.")

if __name__ == "__main__":

    async def main():
        stop_task = asyncio.create_task(stop_bot())
        async with bot:
            load_hidden_commands(bot)
            try:
                print("Adding and syncing slash commands...")

                print("\n+ ---------------------------------------------------------------------- +")
                command_counter = 0
                for command in COMMANDS:
                    command_counter += 1
                    await bot.add_cog(command(bot))
                    print(f"|  {command_counter}.  Command {command.__name__} has been synced to the bot.")
                print("+ ---------------------------------------------------------------------- +")

            except Exception as e:
                print(f"Failed to sync commands: {e}")

            await bot.start(bot_token)

        await stop_task

    asyncio.run(main())

input("\nPress enter to close this window...")
