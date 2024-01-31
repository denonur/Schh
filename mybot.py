import os
import asyncio
import json
import time
import random
import importlib
import sys
from highrise import ResponseError
import requests 
import curses
import discord
import contextlib
import random
from typing import Any, Dict, Union
from highrise import *
from highrise.models import *
from highrise.webapi import *
from highrise.models_webapi import *
from functions.equip import equip
from functions.color import color
from functions.come import come_command
from functions.follow import follow, stop
from functions.reactions import send_reaction
from functions.remove import remove
from functions.promote import promote_user
from functions.move import move_user
from functions.uptime import uptime_command
from functions.userinfo import userinfo
from functions.ping import ping_handler
from functions.summon import summon
from functions.print import print_user_position
from highrise.models import User, Position
from functions.say import SayCommand
from functions.teleport import TeleportCommand
from keep_alive import keep_alive

intents = discord.Intents.default()  # Create default intents
intents.typing = False  # Disable typing event to reduce unnecessary traffic
cooldowns = {}  # Class-level variable to store cooldown timestamps
emote_looping = False

class MyBot(BaseBot):
    continuous_emote_tasks: Dict[int, asyncio.Task[Any]] = {}  
    user_data: Dict[int, Dict[str, Any]] = {}
    EMOTE_DICT = {
      "angry"           : "emoji-angry",
      "bow"             : "emote-bow",
      "casual"          : "idle-dance-casual",
      "charging"        : "emote-charging",
      "confusion"       : "emote-confused",
      "cursing"         : "emoji-cursing",
      "curtsy"          : "emote-curtsy",
      "cutey"           : "emote-cutey",
      "dont"            : "dance-tiktok2",
      "emotecute"       : "emote-cute",
      "energyball"      : "emote-energyball",
      "enthused"        : "idle-enthusiastic",
      "fashionista"     : "emote-fashionista",
      "flex"            : "emoji-flex",
      "flirtywave"      : "emote-lust",
      "float"           : "emote-float",
      "frog"            : "emote-frog",
      "gravedance"      : "dance-weird",
      "gravity"         : "emote-gravity",
      "greedy"          : "emote-greedy",
      "hello"           : "emote-hello",
      "hot"             : "emote-hot",
      "icecream"        : "dance-icecream",
      "kiss"            : "emote-kiss",
      "kpop"            : "dance-blackpink",
      "lambi"           : "emote-superpose",
      "laugh"           : "emote-laughing",
      "letsgo"          : "dance-shoppingcart",
      "maniac"          : "emote-maniac",
      "model"           : "emote-model",
      "no"              : "emote-no",
      "ogdance"         : "dance-macarena",
      "pennydance"      : "dance-pennywise",      
      "pose1"           : "emote-pose1",
      "pose2"           : "emote-pose3",
      "pose3"           : "emote-pose5",
      "pose4"           : "emote-pose7",
      "pose5"           : "emote-pose8",
      "punkguitar"      : "emote-punkguitar",
      "raisetheroof"    : "emoji-celebrate",
      "russian"         : "dance-russian",
      "sad"             : "emote-sad",
      "savage"          : "dance-tiktok8",
      "shuffle"         : "dance-tiktok10",
      "shy"             : "emote-shy",
      "singalong"       : "idle_singing",
      "sit"             : "idle-loop-sitfloor",
      "snowangel"       : "emote-snowangel",
      "snowball"        : "emote-snowball",
      "swordfight"      : "emote-swordfight",
      "telekinesis"     : "emote-telekinesis",
      "teleport"        : "emote-teleporting",
      "thumbsup"        : "emoji-thumbsup",
      "tired"           : "emote-tired",
      "tummyache"       : "emoji-gagging",
      "viral"           : "dance-tiktok9",
      "wave"            : "emote-wave",
      "weird"           : "dance-weird",
      "worm"            : "emote-snake",
      "wrong"           : "dance-wrong",
      "yes"             : "emote-yes",
      "zombierun"       : "emote-zombierun",
      "ANGRY"           : "emoji-angry",
      "BOW"             : "emote-bow",
      "CASUAL"          : "idle-dance-casual",
      "CHARGING"        : "emote-charging",
      "CONFUSION"       : "emote-confused",
      "CURSING"         : "emoji-cursing",
      "CURTSY"          : "emote-curtsy",
      "CUTEY"           : "emote-cutey",
      "DONT"            : "dance-tiktok2",
      "EMOTECUTE"       : "emote-cute",
      "ENERGYBALL"      : "emote-energyball",
      "ENTHUSED"        : "idle-enthusiastic",
      "FASHION"     : "emote-fashionista",
      "FLEX"            : "emoji-flex",
      "FLIRT"      : "emote-lust",
      "FLOAT"           : "emote-float",
      "FROG"            : "emote-frog",
      "GRAVE"      : "dance-weird",
      "GRAVITY"         : "emote-gravity",
      "GREEDY"          : "emote-greedy",
      "HELLO"           : "emote-hello",
      "HOT"             : "emote-hot",
      "ICECREAM"        : "dance-icecream",
      "KISS"            : "emote-kiss",
      "KPOP"            : "dance-blackpink",
      "LAMBI"           : "emote-superpose",
      "LAUGH"           : "emote-laughing",
      "LETSGO"          : "dance-shoppingcart",
      "MANIAC"          : "emote-maniac",
      "MODEL"           : "emote-model",
      "NO"              : "emote-no",
      "MACARENA"         : "dance-macarena",
      "PENNY"      : "dance-pennywise",
      "POSE1"           : "emote-pose1",
      "POSE2"           : "emote-pose3",
      "POSE3"           : "emote-pose5",
      "POSE4"           : "emote-pose7",
      "POSE5"           : "emote-pose8",
      "PUNK"      : "emote-punkguitar",
      "RAISETHEROOF"    : "emoji-celebrate",
      "RUSSIAN"         : "dance-russian",
      "SAD"             : "emote-sad",
      "SAVAGE"          : "dance-tiktok8",
      "SHUFFLE"         : "dance-tiktok10",
      "SHY"             : "emote-shy",
      "SINGALONG"       : "idle-singing",
      "SIT"             : "idle-loop-sitfloor",
      "SNOWANGEL"       : "emote-snowangel",
      "SNOWBALL"        : "emote-snowball",
      "SWORDFIGHT"      : "emote-swordfight",
      "TELEKINESIS"     : "emote-telekinesis",
      "TELEPORT"        : "emote-teleporting",
      "THUMBSUP"        : "emoji-thumbsup",
      "TIRED"           : "emote-tired",
      "TUMMYACHE"       : "emoji-gagging",
      "VIRAL"           : "dance-tiktok9",
      "Wave"            : "emote-wave",
      "Weird"           : "dance-weird",
      "WormM"            : "emote-snake",
      "WrongG"           : "dance-wrong",
      "YES"             : "emote-yes",
      "zombie"       : "emote-zombierun",  
      "Angry"           : "emoji-angry",
      "Bow"             : "emote-bow",
      "Casual"          : "idle-dance-casual",
      "Charging"        : "emote-charging",
      "Confusion"       : "emote-confused",
      "Cursing"         : "emoji-cursing",
      "Curtsy"          : "emote-curtsy",
      "Cutey"           : "emote-cutey",
      "Dontstartnow"            : "dance-tiktok2",
      "Emotecute"       : "emote-cute",
      "Energyball"      : "emote-energyball",
      "Enthused"        : "idle-enthusiastic",
      "Fashionista"     : "emote-fashionista",
      "Flex"            : "emoji-flex",
      "Flirt"      : "emote-lust",
      "Float"           : "emote-float",
      "Frog"            : "emote-frog",
      "Gravedance"      : "dance-weird",
      "Gravity"         : "emote-gravity",
      "Greedy"          : "emote-greedy",
      "Hello"           : "emote-hello",
      "Hot"             : "emote-hot",
      "Icecream"        : "dance-icecream",
      "Kiss"            : "emote-kiss",
      "Kpop"            : "dance-blackpink",
      "Lambi"           : "emote-superpose",
      "Laugh"           : "emote-laughing",
      "Letsgo"          : "dance-shoppingcart",
      "Maniac"          : "emote-maniac",
      "Model"           : "emote-model",
      "No"              : "emote-no",
      "Ogdance"         : "dance-macarena",
      "Pennywise"      : "dance-pennywise",
      "Pose1"           : "emote-pose1",
      "Pose2"           : "emote-pose3",
      "Pose3"           : "emote-pose5",
      "Pose4"           : "emote-pose7",
      "Pose5"           : "emote-pose8",
      "Punk"      : "emote-punkguitar",
      "Raisetheroof"    : "emoji-celebrate",
      "Russian"         : "dance-russian",
      "Sad"             : "emote-sad",
      "Savage"          : "dance-tiktok8",
      "Shuffle"         : "dance-tiktok10",
      "Shy"             : "emote-shy",
      "Singalong"       : "idle-singing",
      "Sit"             : "idle-loop-sitfloor",
      "Snowangel"       : "emote-snowangel",
      "Snowball"        : "emote-snowball",
      "Swordfight"      : "emote-swordfight",
      "Telekinesis"     : "emote-telekinesis",
      "Teleport"        : "emote-teleporting",
      "Thumbsup"        : "emoji-thumbsup",
      "Tired"           : "emote-tired",
      "Gagging"       : "emoji-gagging",
      "Viral"           : "dance-tiktok9",
      "Wave"            : "emote-wave",
      "Weird"           : "dance-weird",
      "Worm"            : "emote-snake",
      "Wrong"           : "dance-wrong",
      "Yes"             : "emote-yes",
      "Zombierun"       : "emote-zombierun",
      "sayso"           : "idle-dance-tiktok4",
      "Sayso"           : "idle-dance-tiktok4",
      "SAYSO"           : "idle-dance-tiktok4",
      "uwu"             : "idle-uwu",
      "UWU"             : "idle-uwu",
      "Uwu"             : "idle-uwu",
    }
    continuous_emote_task = None
    def __init__(self):
        super().__init__()
        # Load emotes from emote.json
        with open("emote.json", "r") as emote_file:
            self.EMOTE_JSON = json.load(emote_file)
        self.preprocessed_emotes = {cmd.lower(): emote_id for cmd, emote_id in self.EMOTE_JSON.items()}
        self.continuous_emote_tasks = {}
        # Initialize user data dictionary
        self.joined_users = []  # List to store joined user data
        self.user_reactions = {}
        self.command_modules = {}  # A dictionary to store the loader
        self.start_time = time.time()
        self.room_dictionary = {
            "room_1": "656cca398287e2f520bc1e95",
            "room_2": "<insert here your room id>",
        }
        self.developer_usernames = ["OnurV", "Atekinz" "", ""]
        self.allowed_usernames = ["OnurV", "LilrodneyBTD", "HimHoodie", "Spydra616", "Punk_Jamie", "Pastel_cloud1", "isStupid", "Milkc0re", "Atekinz"]  # Add more usernames to this list if needed

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

    def load_emotes(self):
        # Load emotes from emote.json
        with open("emote.json", "r") as emote_file:
            self.EMOTE_DICT = json.load(emote_file)

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        try:
            conversations = await self.highrise.get_conversations()
            print(conversations)
            self.uptime = time.time()
            await self.highrise.chat("HEY! My Daddy @Atekinz !!")
            self.highrise.tg.create_task(self.highrise.teleport(session_metadata.user_id, Position(2, 0, 2, "FrontRight")))
        except Exception as e:
            print(f"An exception occurred during on_start: {e}")

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        try:
            privileges = await self.highrise.get_room_privilege(user.id)
            self.joined_users.append(user)
            print(f"{user.username} joined the room with the privileges {privileges}")
            entry_message = [
                f"{user.username} Welcome HR School! 📖"     
            ]
            random_word = random.choice(entry_message)
            await self.highrise.chat(f"{random_word}")
            await self.highrise.send_emote(random.choice(['emoji-flex', 'sit-idle-cute', 'idle-loop-aerobics', 'dance-orangejustice', 'emote-float', 'emote-gravity', 'emote-rest']))
            await self.send_random_reactions(user.id, num_reactions=0, delay=0.2)
        except Exception as e:
        # Handle any exceptions here
            print(f"Error: {e}")

    async def on_user_leave(self, user: User) -> None:
        print(f"{user.username} Left the Room")
        await self.highrise.chat(f"{user.username} See you soon! 👋")

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        response = await self.highrise.get_messages(conversation_id)
        message = "" 

        if isinstance(response, GetMessagesRequest.GetMessagesResponse):
            if response.messages:
                message = response.messages[0].content
                print(message)

        if message:
            if message.lower() == "hello":
                commands = [
                "Hello World!",
                "Here is the list of commands...",
                "list",
                "Emotelist"
                  ]
                for command in commands:
                    await self.highrise.send_message(conversation_id, command)
        
        elif message.lower() == "list":
                await self.highrise.send_message(conversation_id, "Here is the emotelist...")
                await self.highrise.send_message(conversation_id,"angry,bow,casual,raisetheroof,charging,confusion,cursing,curtsy,cutey,dont,emotecute,energyball,enthused,fashionista,flex,flirtywave,float,frog,gravedance,gravity,greedy,hello,hot,icecream,kiss,kpop,lambi,laugh,letsgo,maniac,model,no,ogdance,pennydance,pose1,pose2,pose3,pose4,pose5,punkguitar,russian,sad,savage,shuffle,shy,singalong,sit,snowangel,snowball,swordfight,telekinesis,teleport,thumbsup,tired,tummyache,viral,wave,weird,worm,yes,zombierun")
              
        elif message == "I love you":
                await self.highrise.send_message(conversation_id, "I love u too💋")

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        print (f"{sender.username} tipped {receiver.username} an amount of {tip.amount}")

    async def on_chat(self, user: User, message: str) -> None:
        print(f"{user.username}: {message}")
        args = message.split()  # Split the message into words
        # Load emote IDs from emote.json
        with open("emote.json", "r") as f:
            EMOTE_DICT = json.load(f)
        if message in self.EMOTE_DICT:
            emote_id = self.EMOTE_DICT[message]
            await self.highrise.send_emote(emote_id, user.id)

        if message.startswith("Loop"):
            emote_name = message[5:].strip()
            if emote_name in self.EMOTE_DICT:
                emote_id = self.EMOTE_DICT[emote_name]
                delay = 1
                if " " in emote_name:
                    emote_name, delay_str = emote_name.split(" ")
                    if delay_str.isdigit():
                        delay = float(delay_str)

                if user.id in self.continuous_emote_tasks and not self.continuous_emote_tasks[user.id].cancelled():
                    await self.stop_continuous_emote(user.id)

                task = asyncio.create_task(self.send_continuous_emote(emote_id, user.id,delay))
                self.continuous_emote_tasks[user.id] = task  

        elif message.startswith("Stop"):
            if user.id in self.continuous_emote_tasks and not self.continuous_emote_tasks[user.id].cancelled():
                await self.stop_continuous_emote(user.id)

                await self.highrise.chat("Continuous emote has been stopped.")
            else:
                await self.highrise.chat("You don't have an active loop_emote.")
        elif message.lower().startswith("users"):
            room_users = (await self.highrise.get_room_users()).content
            await self.highrise.chat(f"There are {len(room_users)} users in the room")

        # Process emote commands
        if message.startswith("/"):
            parts = message[1:].split()
            if len(parts) >= 1:
                command = parts[0].lower()

                emote_id = EMOTE_DICT.get(command)
                if emote_id:
                    if len(parts) == 1:
                        await self.highrise.send_emote(emote_id, user.id)
                        return
                    elif len(parts) == 2 and parts[1].startswith("@"):  # Handle /emotename @username case
                        target_username = parts[1][1:]

                # Find the target user in the room
                        room_users = await self.highrise.get_room_users()
                        target_user_id = None
                        for target_user, _ in room_users.content:
                            if target_user.username.lower() == target_username.lower():
                                target_user_id = target_user.id
                                break

                        if not target_user_id:
                            await self.highrise.chat("Target user not found, please specify a valid user.")
                            return

                # Send the emote to the target user
                        await self.highrise.send_emote(emote_id, target_user_id)
                        return
                    elif len(parts) == 2 and parts[1].lower() == "all" and user.username in self.allowed_usernames:  # Handle /emotename all case
                # Send the emote to all users in the room
                        room_users = await self.highrise.get_room_users()
                        for target_user, _ in room_users.content:
                            await self.highrise.send_emote(emote_id, target_user.id)
                        return
                    else:
                        await self.highrise.chat("Invalid command format. Please use '/emote <target> <emote_id>'.")
                        return
                else:
                    await self.highrise.chat("Emote not found, please use a valid emote name.")
                    return

        parts = message.split(" ")
        command = parts[0].lower()

        if command == "teleport" and len(parts) >= 3 and user.username in self.allowed_usernames:
            args = parts[1:]
            teleport_cmd = TeleportCommand(self)
            await teleport_cmd.execute(user, args, message)

        if message.lower().startswith("delayed_message") and user.username in self.developer_usernames:
            await self.delayed_message_command(message)

        elif message.lower() == "stop_delayed_message" and user.username in self.developer_usernames:
            await self.stop_delayed_messages()
        
        if message.startswith("come") and user.username in self.allowed_usernames:
            await come_command(user, self.highrise)

        if message.lower().startswith("wallet") and user.username in self.allowed_usernames:
            wallet = (await self.highrise.get_wallet()).content

        # Prepare the wallet information as a formatted string
            wallet_info = "\n".join(f"{item.type}: {item.amount}" for item in wallet)

            await self.highrise.chat(f"The bot wallet contains:\n{wallet_info}")

        #to check users
        if message.lower().startswith("users") and user.username in self.allowed_usernames:
            room_users = (await self.highrise.get_room_users()).content
            await self.highrise.chat(f"There are {len(room_users)} users in the room")

        #TO_BUY ROOM boost 

        if message.lower().startswith("buy_boost") and user.username in self.allowed_usernames:
            response = await self.highrise.buy_room_boost(payment="bot_wallet_only", amount=1)
            print (response)
            await self.highrise.chat(f"The bot have:\n{response}")

        #to buy room voice

        if message.lower().startswith("buy_voice") and user.username in self.allowed_usernames:
            response = await self.highrise.buy_voice_time(payment="bot_wallet_only")
            print (response)
            await self.highrise.chat(f"The bot have:\n{response}")

        if message.startswith("summon") and user.username in self.allowed_usernames:
            parts = message.split()
            if len(parts) >= 2:
                command = parts[0]
                target_username = parts[1][1:] if parts[1].startswith("@") else parts[1]
                await summon(self, user, target_username)
    
        if message.startswith(f"say") and user.username in self.developer_usernames:
            say_command = SayCommand(self)  # Create an instance of SayCommand
            await say_command.execute(user, [], message)

        #to change the colors of items
        parts = message.split(" ")
        if parts[0].lower() == "color" and user.username in self.developer_usernames:
            await color(self, user, message)  # Call the color function from color.py
        
        if message.startswith("userinfo ") and user.username in self.developer_usernames:
            await userinfo(self, user, message)

        if message.lower().startswith("reload ") and user.username in self.developer_usernames:
            module_name = message.lower().split()[1]
            await self.reload_module(user, module_name)

        if message.lower().startswith("ping") and user.username in self.developer_usernames:
            response = await self.handle_ping()

        if message.startswith("print") and user.username in self.allowed_usernames:
            parts = message.split()
            if len(parts) >= 2:
                command = parts[0]
                args = parts[1:]
                await print_user_position(self, user, args)

        if message.lower().lstrip().startswith(("fight", "hug", "flirt", "stars", "gravity", "uwu", "zero","fashion", "icecream", "punk", "wrong", "sayso", "zombie", "cutey", "pose1", "pose3", "pose5", "pose7", "pose8", "dance", "shuffle", "viralgroove", "weird", "russian", "curtsy", "snowball", "sweating", "snowangel", "cute", "worm", "lambi", "sing", "frog", "energyball", "maniac", "teleport", "float", "telekinesis", "enthused", "confused", "charging", "shopping", "bow", "savage", "kpop", "model", "dontstartnow", "pennywise", "flex", "gagging", "greedy", "cursing", "kiss")):
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]
                usernames = [user.username.lower() for user in users]
                parts = message[1:].split()
                args = parts[1:]
        
                if len(args) < 1:
                    await self.highrise.send_whisper(user.id, f"Usage: {parts[0]} <@username>")
                    return
                elif args[0][0] != "@":
                    await self.highrise.send_whisper(user.id, "Invalid user format. Please use '@username'.")
                    return
                elif args[0][1:].lower() not in usernames:
                    await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
                    return
        
                user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
                if not user_id:
                    await self.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
                    return
        

                if message.lower().lstrip().startswith("fight"):
                        await self.highrise.chat(f"\n🥷 @{user.username} And @{args[0][1:]} Fighting Each Other Like Dummies")
                        await self.highrise.send_emote("emote-swordfight", user.id)
                        await self.highrise.send_emote("emote-swordfight", user_id)

                elif message.lower().lstrip().startswith("hug"):
                        await self.highrise.chat(f"\n🫂 @{user.username} And @{args[0][1:]} Hugging Each Other❤️")
                        await self.highrise.send_emote("emote-hug", user.id)
                        await self.highrise.send_emote("emote-hug", user_id)

                elif message.lower().lstrip().startswith("flirt"):
                        await self.highrise.chat(f"\n Hey @{user.username} And @{args[0][1:]} Flirting Each Other 😏❤️")
                        await self.highrise.send_emote("emote-lust", user.id)
                        await self.highrise.send_emote("emote-lust", user_id)

                elif message.lower().lstrip().startswith("stars"):
                        await self.highrise.send_emote("emote-stargazer", user.id)
                        await self.highrise.send_emote("emote-stargazer", user_id)

                elif message.lower().lstrip().startswith("zero"):
                        await self.highrise.send_emote("emote-astronaut", user.id)
                        await self.highrise.send_emote("emote-astronaut", user_id)

                elif message.lower().lstrip().startswith("gravity"):
                        await self.highrise.send_emote("emote-gravity", user.id)
                        await self.highrise.send_emote("emote-gravity", user_id)

                elif message.lower().lstrip().startswith("uwu"):
                        await self.highrise.send_emote("idle-uwu", user.id)
                        await self.highrise.send_emote("idle-uwu", user_id)

                elif message.lower().lstrip().startswith("fashion"):
                        await self.highrise.send_emote("emote-fashionista", user.id)
                        await self.highrise.send_emote("emote-fashionista", user_id)

                elif message.lower().lstrip().startswith("icecream"):
                        await self.highrise.send_emote("dance-icecream", user.id)
                        await self.highrise.send_emote("dance-icecream", user_id)

                elif message.lower().lstrip().startswith("punk"):
                        await self.highrise.send_emote("emote-punkguitar", user.id)
                        await self.highrise.send_emote("emote-punkguitar", user_id)

                elif message.lower().lstrip().startswith("wrong"):
                        await self.highrise.send_emote("dance-wrong", user.id)
                        await self.highrise.send_emote("dance-wrong", user_id)

                elif message.lower().lstrip().startswith("sayso"):
                        await self.highrise.send_emote("idle-dance-tiktok4", user.id)
                        await self.highrise.send_emote("idle-dance-tiktok4", user_id)

                elif message.lower().lstrip().startswith("zombie"):
                        await self.highrise.send_emote("emote-zombierun", user.id)
                        await self.highrise.send_emote("emote-zombierun", user_id)

                elif message.lower().lstrip().startswith("cutey"):
                        await self.highrise.send_emote("emote-cutey", user.id)
                        await self.highrise.send_emote("emote-cutey", user_id)

                elif message.lower().lstrip().startswith("pose5"):
                        await self.highrise.send_emote("emote-pose5", user.id)
                        await self.highrise.send_emote("emote-pose5", user_id)

                elif message.lower().lstrip().startswith("pose3"):
                        await self.highrise.send_emote("emote-pose3", user.id)
                        await self.highrise.send_emote("emote-pose3", user_id)

                elif message.lower().lstrip().startswith("pose1"):
                        await self.highrise.send_emote("emote-pose1", user.id)
                        await self.highrise.send_emote("emote-pose1", user_id)

                elif message.lower().lstrip().startswith("pose7"):
                        await self.highrise.send_emote("emote-pose7", user.id)
                        await self.highrise.send_emote("emote-pose7", user_id)

                elif message.lower().lstrip().startswith("pose8"):
                        await self.highrise.send_emote("emote-pose8", user.id)
                        await self.highrise.send_emote("emote-pose8", user_id)

                elif message.lower().lstrip().startswith("dance"):
                        await self.highrise.send_emote("idle-dance-casual", user.id)
                        await self.highrise.send_emote("idle-dance-casual", user_id)

                elif message.lower().lstrip().startswith("shuffle"):
                        await self.highrise.send_emote("dance-tiktok10", user.id)
                        await self.highrise.send_emote("dance-tiktok10", user_id)

                elif message.lower().lstrip().startswith("weird"):
                        await self.highrise.send_emote("emote-weird", user.id)
                        await self.highrise.send_emote("emote-weird", user_id)

                elif message.lower().lstrip().startswith("viralgroove"):
                        await self.highrise.send_emote("dance-tiktok9", user.id)
                        await self.highrise.send_emote("dance-tiktok9", user_id)
                    
                elif message.lower().lstrip().startswith("cute"):
                        await self.highrise.send_emote("emote-cute", user.id)
                        await self.highrise.send_emote("emote-cute", user_id)

                elif message.lower().lstrip().startswith("frog"):
                        await self.highrise.send_emote("emote-frog", user.id)
                        await self.highrise.send_emote("emote-frog", user_id)

                elif message.lower().lstrip().startswith("lambi"):
                        await self.highrise.send_emote("emote-superpose", user.id)
                        await self.highrise.send_emote("emote-superpose", user_id)

                elif message.lower().lstrip().startswith("sing"):
                        await self.highrise.send_emote("idle-singing", user.id)
                        await self.highrise.send_emote("idle-singing", user_id)

                elif message.lower().lstrip().startswith("worm"):
                        await self.highrise.send_emote("emote-snake", user.id)
                        await self.highrise.send_emote("emote-snake", user_id)

                elif message.lower().lstrip().startswith("bow"):
                        await self.highrise.send_emote("emote-bow", user.id)
                        await self.highrise.send_emote("emote-bow", user_id)

                elif message.lower().lstrip().startswith("energyball"):
                        await self.highrise.send_emote("emote-energyball", user.id)
                        await self.highrise.send_emote("emote-energyball", user_id)

                elif message.lower().lstrip().startswith("maniac"):
                        await self.highrise.send_emote("emote-maniac", user.id)
                        await self.highrise.send_emote("emote-maniac", user_id)

                elif message.lower().lstrip().startswith("teleport"):
                        await self.highrise.send_emote("emote-teleporting", user.id)
                        await self.highrise.send_emote("emote-teleporting", user_id)

                elif message.lower().lstrip().startswith("float"):
                        await self.highrise.send_emote("emote-float", user.id)
                        await self.highrise.send_emote("emote-float", user_id)

                elif message.lower().lstrip().startswith("telekinesis"):
                        await self.highrise.send_emote("emote-telekinesis", user.id)
                        await self.highrise.send_emote("emote-telekinesis", user_id)

                elif message.lower().lstrip().startswith("enthused"):
                        await self.highrise.send_emote("idle-enthusiastic", user.id)
                        await self.highrise.send_emote("idle-enthusiastic", user_id)

                elif message.lower().lstrip().startswith("confused"):
                        await self.highrise.send_emote("emote-confused", user.id)
                        await self.highrise.send_emote("emote-confused", user_id)

                elif message.lower().lstrip().startswith("shopping"):
                        await self.highrise.send_emote("dance-shoppingcart", user.id)
                        await self.highrise.send_emote("dance-shoppingcart", user_id)

                elif message.lower().lstrip().startswith("charging"):
                        await self.highrise.send_emote("emote-charging", user.id)
                        await self.highrise.send_emote("emote-charging", user_id)

                elif message.lower().lstrip().startswith("snowangel"):
                        await self.highrise.send_emote("emote-snowangel", user.id)
                        await self.highrise.send_emote("emote-snowangel", user_id)

                elif message.lower().lstrip().startswith("sweating"):
                        await self.highrise.send_emote("emote-hot", user.id)
                        await self.highrise.send_emote("emote-hot", user_id)

                elif message.lower().lstrip().startswith("snowball"):
                        await self.highrise.send_emote("emote-snowball", user.id)
                        await self.highrise.send_emote("emote-snowball", user_id)

                elif message.lower().lstrip().startswith("curtsy"):
                        await self.highrise.send_emote("emote-curtsy", user.id)
                        await self.highrise.send_emote("emote-curtsy", user_id)

                elif message.lower().lstrip().startswith("russian"):
                        await self.highrise.send_emote("dance-russian", user.id)
                        await self.highrise.send_emote("dance-russian", user_id)

                elif message.lower().lstrip().startswith("pennywise"):
                        await self.highrise.send_emote("dance-pennywise", user.id)
                        await self.highrise.send_emote("dance-pennywise", user_id)

                elif message.lower().lstrip().startswith("dontstartnow"):
                        await self.highrise.send_emote("dance-tiktok2", user.id)
                        await self.highrise.send_emote("dance-tiktok2", user_id)

                elif message.lower().lstrip().startswith("kpop"):
                        await self.highrise.send_emote("dance-blackpink", user.id)
                        await self.highrise.send_emote("dance-blackpink", user_id)

                elif message.lower().lstrip().startswith("model"):
                        await self.highrise.send_emote("emote-model", user.id)
                        await self.highrise.send_emote("emote-model", user_id)

                elif message.lower().lstrip().startswith("savage"):
                        await self.highrise.send_emote("dance-tiktok8", user.id)
                        await self.highrise.send_emote("dance-tiktok8", user_id)

                elif message.lower().lstrip().startswith("flex"):
                        await self.highrise.send_emote("emoji-flex", user.id)
                        await self.highrise.send_emote("emoji-flex", user_id)

                elif message.lower().lstrip().startswith("gagging"):
                        await self.highrise.send_emote("emoji-gagging", user.id)
                        await self.highrise.send_emote("emoji-gagging", user_id)

                elif message.lower().lstrip().startswith("greedy"):
                        await self.highrise.send_emote("emote-greedy", user.id)
                        await self.highrise.send_emote("emote-greedy", user_id)

                elif message.lower().lstrip().startswith("cursing"):
                        await self.highrise.send_emote("emoji-cursing", user.id)
                        await self.highrise.send_emote("emoji-cursing", user_id)

                elif message.lower().lstrip().startswith("kiss"):
                        await self.highrise.send_emote("emote-kiss", user.id)
                        await self.highrise.send_emote("eote-kiss", user_id)

        #Reaction

        if message.startswith("❤"):
            await self.highrise.react("heart", user.id)
        if message.startswith("Sa"):
            await self.highrise.react("wave", user.id)
        if message.startswith("👏"):
            await self.highrise.react("clap", user.id)
        if message.startswith("👍"):
            await self.highrise.react("thumbs", user.id)
        if message.startswith("😉"):
            await self.highrise.react("wink", user.id)

        if user.username not in self.allowed_usernames:
            return

        if message.startswith('❤'):
            reaction_type = "heart"
            count = message[2:].strip()
            await send_reaction(user, self.highrise, reaction_type, count)

        elif message.startswith("wave"):
            reaction_type = "wave"
            count = message[2:].strip()
            await send_reaction(user, self.highrise, reaction_type, count)

        elif message.startswith("clap"):
            reaction_type = "clap"
            count = message[2:].strip()
            await send_reaction(user, self.highrise, reaction_type, count)

        elif message.startswith("thumbsup"):
            reaction_type = "thumbsup"
            count = message[2:].strip()
            await send_reaction(user, self.highrise, reaction_type, count)

        elif message.startswith("wink"):
            reaction_type = "wink"
            count = message[2:].strip()
            await send_reaction(user, self.highrise, reaction_type, count)

        if message.lower().startswith("buy ") and user.username in self.developer_usernames:
            parts = message.split(" ")
            if len(parts) != 2:
                await self.highrise.chat("Invalid command")
                return
            item_id = parts[1]
            try:
                response = await self.highrise.buy_item(item_id)
                await self.highrise.chat(f"Item bought: {response}")
            except Exception as e:
                await self.highrise.chat(f"Error: {e}")

        #the bot will equip  outfit
        if user.username in self.allowed_usernames:
            parts = message.split(" ")
            if parts[0].lower() == "equip" and user.username in self.developer_usernames:
                await self.equip(user, message)  # Call the equip method on the bot instance
        
        if message.startswith("remove") and user.username in self.developer_usernames:
            await remove(self, user, message) 
        
        if message.lower().startswith("follow") and user.username in self.developer_usernames:
            await follow(self, user, message)

        # Check if the user wants to stop following
        elif message.lower().startswith("stop") and user.username in self.developer_usernames:
            await stop(self, user, message)

        if message.startswith("promote") and user.username in self.allowed_usernames:
            await promote_user(self, message, user)

        if message.startswith("move") and user.username in self.developer_usernames:
            await move_user(self, message, user)

        if message.startswith("uptime") and user.username in self.developer_usernames:
                await uptime_command(self, user, message)

        if message.lower().lstrip().startswith('fly'):
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]
            usernames = [user.username.lower() for user in users]
            parts = message[1:].split()
            args = parts[1:]

            if len(args) < 1:
                await self.highrise.send_whisper(user.id, "Usage: fly <position>")
                return

            position_name = " ".join(args)
            if position_name == 'down':
                dest = Position(12.0, 0.0, 27.0)
            elif position_name == 'floor1':
                dest = Position(11.5, 8.5, 26.5)
            elif position_name == 'floor2':
                dest = Position(11.0, 19.0, 26.5)
            elif position_name == 'disco':
                dest = Position(5.5, 0.25, 5.5)
            elif position_name == '':
                dest = Position(17, -5, 5)

            else:
                return await self.highrise.send_whisper(user.id, "Unknown location")

            user_id = user.id  # Use the ID of the user who sent the command
            await self.highrise.teleport(user_id, dest)

            await self.highrise.send_whisper(user.id, f"Flew to {position_name}: ({dest.x}, {dest.y}, {dest.z})")
        else:
            pass
          
        if message.lower().lstrip().startswith(("!invite", "-invite")):
                parts = message[1:].split()
                args = parts[1:]
                _bid = "6460d4038907b9356ffaf9ae" #Bot user.id here
                id = f"1_on_1:{_bid}:{user.id}"
                idx = f"1_on_1:{user.id}:{_bid}"
                rid = "6505a4d31aa3dee29ea261c4" #Room ID Here

                if len(args) < 1:
                    await self.highrise.send_whisper(user.id, "\nUsage: !invite <@username> or -invite <@username> This command will send room invite to targeted username. if they ever interact with our bot in past\n • Example: !invite @_y_17")
                    return
                elif args[0][0] != "@":
                    await self.highrise.send_whisper(user.id, "Invalid user format. Please use '@username'.")
                    return

                url = f"https://webapi.highrise.game/users?&username={args[0][1:]}&sort_order=asc&limit=1"
                response = requests.get(url)
                data = response.json()
                users = data['users']
                
                for user in users:
                    user_id = user['user_id']
                    __id = f"1_on_1:{_bid}:{user_id}"
                    __idx = f"1_on_1:{user_id}:{_bid}"
                    __rid = "6505a4d31aa3dee29ea261c4" #Room ID Here
                    try:
                        await self.highrise.send_message(__id, "Join Room", "invite", __rid)
                    except:
                        await self.highrise.send_message(__idx, "Join Room", "invite", __rid)

         #command list for moderations.

        command_prefix = "."  # Set your desired command prefix here
        command_list = [
            {"command": "kick", "function": self.kick_user, "description": "kicked"},
            {"command": "ban", "function": self.ban_user, "description": "banned"},
            {"command": "unban", "function": self.unban_user, "description": "unbanned"},
            {"command": "mute", "function": self.mute_user, "description": "muted"},
            {"command": "unmute", "function": self.unmute_user, "description": "unmuted"},
        ]

        parts = message.split()

        if not message.startswith(command_prefix) and user.username in self.allowed_usernames:
            return

        if len(parts) < 2:
            await self.highrise.chat("Invalid command format.")
            return

        for command_info in command_list:
            if message.startswith(f"{command_prefix}{command_info['command']}"):
                await command_info["function"](user, message)
                return

    # Debugging statements
        print(f"Command not recognized: {message}")
        await self.highrise.chat("Command not recognized.")

    async def equip(self, user: User, message: str):
        await equip(self, user, message)  # Pass 'self' as the first parameter to the equip method

    async def handle_follow(self, user: User, message: str) -> None:
        # Implement any checks or additional logic here if needed
        await follow(self, user, message)
        # Creating a task for following_loop and suppressing the warning

    async def handle_stop(self, user: User, message: str) -> None:
        # Implement any checks or additional logic here if needed
        await stop(self, user, message)

    #kick command handler

    async def kick_user(self, user: User, message: str) -> None:
        if user.username in self.allowed_usernames:
            pass
        else:
            await self.highrise.chat("You do not have permission to use this command.")
            return

        parts = message.split()

        if len(parts) != 2:
            await self.highrise.chat("Invalid kick command format.")
            return

        if "@" not in parts[1]:
            username = parts[1]
        else:
            username = parts[1][1:]

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                user_id = room_user.id
                break

        if "user_id" not in locals():
            await self.highrise.chat("User not found, please specify a valid user.")
            return

        try:
            await self.highrise.moderate_room(user_id, "kick")
        except Exception as e:
            await self.highrise.chat(f"{e}")
            return

        await self.highrise.chat(f"{username} has been kicked from the room.")

        #Ban Handler
    
    async def ban_user(self, user: User, message: str) -> None:
        if user.username in self.allowed_usernames:
            pass
        else:
            self.highrise.chat("You do not have permission to use this command.")
            return

        parts = message.split()

        if len(parts) != 2:
            await self.highrise.chat("Invalid Ban command format.")
            return

        if "@" not in parts[1]:
            username = parts[1]
        else:
            username = parts[1][1:]

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                user_id = room_user.id
                break

        if "user_id" not in locals():
            await self.highrise.chat("User not found, please specify a valid user.")
            return
    # Replace the "moderate_room" call with the ban action
        try:
            await self.highrise.moderate_room(user_id, "ban")
        except Exception as e:
            await self.highrise.chat(f"{e}")
            return

        await self.highrise.chat(f"{username} has been banned from the room.")

    #Unban handler

    async def unban_user(self, user: User, message: str) -> None:
        if user.username in self.allowed_usernames:
            pass
        else:
            self.highrise.chat("You do not have permission to use this command.")
            return

        parts = message.split()

        if len(parts) != 2:
            await self.highrise.chat("Invalid Unban command format.")
            return

        if "@" not in parts[1]:
            username = parts[1]
        else:
            username = parts[1][1:]

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                user_id = room_user.id
                break

        if "user_id" not in locals():
            await self.highrise.chat("User not found, please specify a valid user.")
            return
    # Replace the "moderate_room" call with the unban action
        try:
            await self.highrise.moderate_room(user_id, "unban")
        except Exception as e:
            await self.highrise.chat(f"{e}")
            return

        await self.highrise.chat(f"{username} has been unbanned.")

    async def mute_user(self, user: User, message: str) -> None:
        if user.username in self.allowed_usernames:
            pass
        else:
            self.highrise.chat("You do not have permission to use this command.")
            return

        parts = message.split()

        if len(parts) != 2:
            await self.highrise.chat("Invalid Mute command format.")
            return

        if "@" not in parts[1]:
            username = parts[1]
        else:
            username = parts[1][1:]

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                user_id = room_user.id
                break

        if "user_id" not in locals():
            await self.highrise.chat("User not found, please specify a valid user.")
            return
        try:
            await self.highrise.moderate_room(user_id, "mute")
        except Exception as e:
            await self.highrise.chat(f"{e}")
            return

        await self.highrise.chat(f"{username} has been muted.")

    async def unmute_user(self, user: User, message: str) -> None:
        if user.username in self.allowed_usernames:
            pass
        else:
            self.highrise.chat("You do not have permission to use this command.")
            return

        parts = message.split()

        if len(parts) != 2:
            await self.highrise.chat("Invalid Unmute command format.")
            return

        if "@" not in parts[1]:
            username = parts[1]
        else:
            username = parts[1][1:]

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                user_id = room_user.id
                break

        if "user_id" not in locals():
            await self.highrise.chat("User not found, please specify a valid user.")
            return
        try:
            await self.highrise.moderate_room(user_id, "unmute")
        except Exception as e:
            await self.highrise.chat(f"{e}")
            return
        
    async def handle_ping(self):
        return await ping_handler(self.highrise)
    
    from highrise.models import User, Position
 
    async def reload_module(self, user, module_name):
        try:
            if module_name == "mybot":
                # If module_name is "mybot", reload the MyBot class and its attributes
                importlib.reload(sys.modules[__name__])
                bot = MyBot()  # Create a new instance of the reloaded MyBot class
                self.__dict__.update(bot.__dict__)  # Update the current instance with the new attributes
                await self.highrise.send_whisper(user.id, f"{module_name} reloaded successfully.")
            else:
                # For other module names, attempt to reload the command module
                module_path = f"events.{module_name}"
                if module_path in sys.modules:
                    module = importlib.reload(sys.modules[module_path])
                    self.command_modules[module_name] = module
                    await self.highrise.send_whisper(user.id, f"Module '{module_name}' reloaded successfully.")
                else:
                    await self.highrise.send_whisper(user.id, f"Module '{module_name}' not found.")

        except Exception as e:
            await self.highrise.send_whisper(user.id, f"Failed to reload module '{module_name}': {str(e)}")
            
    from highrise.models import User, Position

    async def stop_continuous_emote(self, user_id: int):
        if user_id in self.continuous_emote_tasks and not self.continuous_emote_tasks[user_id].cancelled():
            task = self.continuous_emote_tasks[user_id]
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
            del self.continuous_emote_tasks[user_id]

    async def send_continuous_emote(self, emote_id: str, user_id: int, delay: float):
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(delay)
        except ConnectionResetError:
            print(f"Failed to send continuous emote to user {user_id}. Connection was reset.")
        except asyncio.CancelledError:
            print(f"Continuous emote task for user {user_id} was cancelled.")
        except ResponseError as error:
            if str(error) == "Target user not in room":
                print(f"User {user_id} is not in the room.")
            else:
                raise  # Re-raise the exception if it's not the one we're handling.

    async def delayed_message_command(self, command: str):
        try:
            _, delay_str, *message_parts = command.split()
            delay = int(delay_str)
            message = " ".join(message_parts)

            await self.highrise.chat(f"Bot will send '{message}' every {delay} seconds.")

            # Start the delayed message loop as a background task
            self.stop_delayed_messages_received = False
            self.bot_loop_task = asyncio.create_task(self.delayed_message_loop(delay, message))
        except ValueError:
            await self.highrise.chat("Invalid command. Usage: delayed_message <delay_seconds> <message>")
        except Exception as e:
            await self.highrise.chat(f"An error occurred: {str(e)}")

    async def delayed_message_loop(self, delay: int, message: str):
        while not self.stop_delayed_messages_received:
            await asyncio.sleep(delay)
            await self.highrise.chat(message)

    async def stop_delayed_messages(self):
        # Stop the delayed message loop
        self.stop_delayed_messages_received = True
        await self.bot_loop_task  # Wait for the loop task to complete
        await self.highrise.chat("Delayed messages have been stopped.")
                  
    async def get_user_data(self, user_id: str) -> dict:
      if user_id not in self.user_data:
          self.user_data[user_id] = {}  # Initialize empty data for new users
      return self.user_data[user_id]

    async def send_random_reactions(self, user_id: str, num_reactions: int = 20, delay: float = 0.2) -> None:
        reactions = ["heart"]
        for _ in range(num_reactions):
            reaction = random.choice(reactions)
            await self.highrise.react(reaction, user_id)
            await asyncio.sleep(delay)  # Add a delay between reactions
    
    if __name__ == "__main__":
      keep_alive()
