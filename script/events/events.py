import asyncio
import aiohttp
import random
import re
import datetime
import time
import json
import os

import discord
from discord.ext import commands
from USEFUL_IDS import ID_LOGS, ID_CADET_CLONE_TROOPER_ROLE, ID_COMPTE_DE_SESSION, ID_HELPER, IDS_WHITE_LISTES



intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

cooldowns = {}


def read_file(file):
    with open(f'script/events/banned_member_folder/{file}', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [int(line.split(';')[1].strip()) for line in lines]


list_banned_community_member = read_file('list_banned_community_member.txt')

list_banned_chat_member = read_file('list_banned_chat_member.txt')
list_banned_voice_member = read_file('list_banned_voice_member.txt')
list_banned_reaction_member = read_file('list_banned_reaction_member.txt')

URL_FILE = "urls.json"


def setup_events(bot: commands.Bot):

    async def cycle_status_messages():
        default_status_messages = [
            discord.Game(name="/display-commands"),
            discord.Game(name="Human Simulator II"),
            discord.Game(name="codé par Wivex"),
            discord.Activity(type=discord.ActivityType.listening, name="The Imperial March"),
            discord.Activity(type=discord.ActivityType.watching, name="STAR WARS III"),
        ]
        default_bot_status = [
            discord.Status.idle,
            discord.Status.do_not_disturb,
            discord.Status.online
        ]

        while True:
            for status_message in default_status_messages:
                await bot.change_presence(
                    status=random.choice(default_bot_status),
                    activity=status_message
                )
                await asyncio.sleep(30)

    @bot.event
    async def on_ready():
        print(f'Bot is connected to Discord :\n\n> Name: {bot.user.name}\n> ID: {bot.user.id}')
        asyncio.create_task(cycle_status_messages())

        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} slash commands with Discord.\n")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    @bot.event
    async def on_message(message):

        dict_ref = [
            {
                "channel_id": 962314938079121428,
                "message_triggering": "roger roger",
                "message_to_send": "https://tenor.com/view/droid-b1-gif-19907265"
            },
            {
                "channel_id": 962314938079121428,
                "message_triggering": "i am your father",
                "message_to_send": "https://tenor.com/view/yes-gif-19665261"
            },
            {
                "channel_id": 962314938079121428,
                "message_triggering": "what's happening",
                "message_to_send": "https://tenor.com/view/capitaine-rex-ahsoka-tano-the-clone-wars-execute-order-66-gif-5097545684667501624"
            },
            {
                "channel_id": 962314938079121428,
                "message_triggering": "may the 4 be with you",
                "message_to_send": "https://tenor.com/view/may-the4th-may-the-fourth-stormtrooper-dance-dancing-gif-17104311"
            },
            {
                "channel_id": 962314938079121428,
                "message_triggering": "i am your father",
                "message_to_send": "https://tenor.com/view/yes-gif-19665261"
            }
        ]

        CHANNEL_LOGS = bot.get_channel(ID_LOGS)

        async def check_link():
            white_list_link_list = [
                "discord.gg/1",
                "vm.tiktok.com/",
            ]

            url_regex = r'(https?://[^\s]+|(?:\w+\.)+\w{2,})'

            if message.author.bot:
                return

            message_content = message.content.lower()

            found_links = re.findall(url_regex, message_content)

            if found_links:
                detected_links = [link.replace("https://", "").replace("http://", "") for link in found_links]

                authorized_links = [link for link in detected_links if
                                    any(link.startswith(wl) for wl in white_list_link_list)]

                if len(authorized_links) < len(detected_links):
                    try:
                        log_channel = bot.get_channel(1356672819211014334)

                        embed = discord.Embed(
                            color=discord.Color.dark_red()
                        )

                        embed.set_author(
                            name="Auteur :",
                            icon_url=message.author.avatar.url if message.author.avatar else None
                        )

                        embed.add_field(name="", value=f"**➪** {message.author.mention}", inline=False)
                        embed.add_field(name="", value=f"**➪** {message.author.name}", inline=False)

                        embed.add_field(
                            name="# Message :",
                            value=message.content if len(message.content) < 1024 else message.content[:1020] + "...",
                            inline=False
                        )

                        embed.add_field(
                            name="# Salon :",
                            value=f"**➪** {message.channel.mention}\n**➪** {message.channel.name}",
                            inline=False
                        )

                        unix_ts = int(datetime.datetime.now().timestamp())
                        embed.add_field(name=f"~ <t:{unix_ts}:R> ~", value="", inline=False)

                        await log_channel.send(embed=embed)
                        await message.delete()

                    except Exception as e:
                        print(f"Erreur : {e}")

        # FOR BANNED PEOPLE COMMUNITY
        for banned_member in list_banned_community_member:
            dt = datetime.datetime.now()
            unix_timestamp = int(time.mktime(dt.timetuple()))
            if banned_member == message.author.id:
                try:
                    print(f'Message supprimé de {message.author.name}: {message.content}')
                    embed_delete_message = discord.Embed(color=discord.Color.dark_red())
                    embed_delete_message.add_field(
                        name=f"Message supprimé de {message.author.name}\nᅠ\n",
                        value=f"➪ <@{message.author.id}>\n\n➪ **Message:** {message.content}\n\n➪ **Salon:** <#{message.channel.id}>\n\n➪ **<t:{unix_timestamp}:R>**",
                        inline=False
                    )
                    embed_delete_message.set_footer(text=f"{message.author.name} est banni de tout intéraction avec la communauté.")
                    await CHANNEL_LOGS.send(embed=embed_delete_message)
                    await message.delete()
                except Exception as e:
                    print(f"Erreur lors de la suppression du message de {message.author.name}: {e}")


        # ONLY FOR PEOPLE BANNED CHAT
        for banned_chat_member in list_banned_chat_member:
            dt = datetime.datetime.now()
            unix_timestamp = int(time.mktime(dt.timetuple()))
            if banned_chat_member == message.author.id:
                try:
                    print(f'Message supprimé de {message.author.name}: {message.content}')
                    embed_delete_message = discord.Embed(color=discord.Color.dark_red())
                    embed_delete_message.add_field(
                        name=f"Message supprimé de {message.author.name}\nᅠ\n",
                        value=f"➪ <@{message.author.id}>\n\n➪ **Message:** {message.content}\n\n➪ **Salon:** <#{message.channel.id}>\n\n➪ **<t:{unix_timestamp}:R>**",
                        inline=False
                    )
                    embed_delete_message.set_footer(text=f"{message.author.name} n'est pas autorisé à envoyer des messages.")
                    await CHANNEL_LOGS.send(embed=embed_delete_message)
                    await message.delete()
                except Exception as e:
                    print(f"Erreur lors de la suppression du message de {message.author.name}: {e}")

        if "you were the chosen one" in message.content.lower().strip() and message.channel.id == 962314938079121428:
            try:

                obiwan_webhook = "https://discord.com/api/webhooks/1370685076651638794/aFamhlc1mxLU0yNS5sLcgYNWM_zb2lz4XUNpzqoPszh7AFJ_CMibRZtIlEokC7Txzv40"
                anakin_webhook = "https://discord.com/api/webhooks/1370687006878990416/Qj3zMjbGDwhcMW0H7ANg-aJfMDCC7khszkUoFUIMg95x2Xlbmv_rIouMwCsq2bYehCyz"

                obiwan_lines = [
                    "It was said that you would destroy the Sith, not join them !",
                    "Bring balance to the Force, not leave it in darkness !",
                    "You were my brother, Anakin.",
                    "I loved you...",
                    "https://tenor.com/view/obiwan-starwars-dissapointment-gif-5299171"
                ]

                anakin_lines = [
                    "https://tenor.com/view/i-hate-you-anakin-star-wars-gif-10358450"
                ]

                async with aiohttp.ClientSession() as session:
                    for line in obiwan_lines:
                        await session.post(obiwan_webhook, json={
                            "content": line
                        })
                        await asyncio.sleep(2.5)

                    for line in anakin_lines:
                        await session.post(anakin_webhook, json={
                            "content": line
                        })
                        await asyncio.sleep(2)
            except Exception as e:
                print(e)

        for rule in dict_ref:
            if rule["channel_id"] == message.channel.id and rule["message_triggering"].lower() in message.content.lower():
                now = time.time()
                last_triggered = cooldowns.get(message.channel.id, 0)

                if now - last_triggered < 180:
                    break

                cooldowns[message.channel.id] = now
                await message.channel.send(rule["message_to_send"])
                await bot.process_commands(message)
                break

        await bot.process_commands(message)

    @bot.event
    async def on_voice_state_update(member, before, after):

        CHANNEL_LOGS = bot.get_channel(ID_LOGS)

        role = discord.utils.get(member.guild.roles, id=ID_HELPER)
        embed_color = role.color if role else discord.Color.default()


        # FOR BANNED PEOPLE COMMUNITY
        for banned_member in list_banned_community_member:
            dt = datetime.datetime.now()
            unix_timestamp = int(time.mktime(dt.timetuple()))
            if before.channel != after.channel and after.channel is not None:
                if banned_member == member.id:
                    try:
                        embed_kick_out_of_voice_channel = discord.Embed(color=discord.Color.dark_red())
                        embed_kick_out_of_voice_channel.add_field(
                            name=f"{member.name} a été déconnecté d'un salon vocal\nᅠ\n",
                            value=f"➪ <@{member.id}>\n\n➪ **Salon:** <#{after.channel.id}>\n\n➪ **<t:{unix_timestamp}:R>**",
                            inline=False
                        )
                        embed_kick_out_of_voice_channel.set_footer(text=f"{member.name} est banni de tout intéraction avec la communauté.")
                        await CHANNEL_LOGS.send(embed=embed_kick_out_of_voice_channel)
                        print(f"{member.name} a été déconnecté de {after.channel.name}.")
                        await member.edit(voice_channel=None)
                    except Exception as e:
                        print(f"Erreur lors de la déconnexion de {member.name} dans le salon {after.channel.name}: {e}")


        # ONLY FOR PEOPLE BANNED VOICE CHANNEL
        for banned_voice_member in list_banned_voice_member:
            dt = datetime.datetime.now()
            unix_timestamp = int(time.mktime(dt.timetuple()))
            if before.channel != after.channel and after.channel is not None:
                if banned_voice_member == member.id:
                    try:
                        embed_kick_out_of_voice_channel = discord.Embed(color=discord.Color.dark_red())
                        embed_kick_out_of_voice_channel.add_field(
                            name=f"{member.name} a été déconnecté d'un salon vocal\nᅠ\n",
                            value=f"➪ <@{member.id}>\n\n➪ **Salon:** <#{after.channel.id}>\n\n➪ **<t:{unix_timestamp}:R>**",
                            inline=False
                        )
                        embed_kick_out_of_voice_channel.set_footer(text=f"{member.name} n'est pas autorisé à rejoindre des salons vocaux.")
                        await CHANNEL_LOGS.send(embed=embed_kick_out_of_voice_channel)
                        print(f"{member.name} a été déconnecté de {after.channel.name}.")
                        await member.edit(voice_channel=None)
                    except Exception as e:
                        print(f"Erreur lors de la déconnexion de {member.name} dans le salon {after.channel.name}: {e}")

    @bot.event
    async def on_reaction_add(reaction, user):
        EVERYTIME_ALLOWED_CHANNEL = [962314997646643220, 962314973214826526, 1004525840056467477, 1100867195707342938, 1078387595584753788, 1100895296613003275, 996213406879187054]


        CHANNEL_LOGS = bot.get_channel(ID_LOGS)


        # FOR BANNED PEOPLE COMMUNITY
        for banned_member in list_banned_community_member:
            for CHANNEL_ALLOWED_ID in EVERYTIME_ALLOWED_CHANNEL:
                if reaction.message.channel.id == CHANNEL_ALLOWED_ID:
                    return
                else:
                    dt = datetime.datetime.now()
                    unix_timestamp = int(time.mktime(dt.timetuple()))
                    if banned_member == user.id:
                        try:
                            await reaction.remove(user)
                            print(f'Réaction {reaction} supprimée de {user.name}')
                            embed_remove_reaction = discord.Embed(color=discord.Color.dark_red())
                            embed_remove_reaction.add_field(
                                name=f"Réaction supprimée de {user.name}\nᅠ\n",
                                value=f"➪ <@{user.id}>\n\n➪ **Réaction:** {reaction}\n\n➪ **Salon:** <#{reaction.message.channel.id}>\n\n➪ **<t:{unix_timestamp}:R>**",
                                inline=False
                            )
                            embed_remove_reaction.set_footer(text=f"{user.name} est banni de tout intéraction avec la communauté.")
                            await CHANNEL_LOGS.send(embed=embed_remove_reaction)
                        except Exception as e:
                            print(f'Erreur lors de la suppression de la réaction {reaction}: {e}')
                        return


        # ONLY FOR PEOPLE BANNED REACTION
        for banned_reaction_member in list_banned_reaction_member:
            for CHANNEL_ALLOWED_ID in EVERYTIME_ALLOWED_CHANNEL:
                if reaction.message.channel.id == CHANNEL_ALLOWED_ID:
                    return
                else:
                    dt = datetime.datetime.now()
                    unix_timestamp = int(time.mktime(dt.timetuple()))
                    if banned_reaction_member == user.id:
                        try:
                            await reaction.remove(user)
                            print(f'Réaction {reaction} supprimée de {user.name}')
                            embed_remove_reaction = discord.Embed(color=discord.Color.dark_red())
                            embed_remove_reaction.add_field(
                                name=f"Réaction supprimée de {user.name}\nᅠ\n",
                                value=f"➪ <@{user.id}>\n\n➪ **Réaction:** {reaction}\n\n➪ **Salon:** <#{reaction.message.channel.id}>\n\n➪ **<t:{unix_timestamp}:R>**",
                                inline=False
                            )
                            embed_remove_reaction.set_footer(text=f"{user.name} n'est pas autorisé à ajouter des réactions.")
                            await CHANNEL_LOGS.send(embed=embed_remove_reaction)
                        except Exception as e:
                            print(f'Erreur lors de la suppression de la réaction {reaction}: {e}')
                        return
