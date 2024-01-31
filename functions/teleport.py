import json
from highrise.models import User, Position

class TeleportCommand:
    def __init__(self, bot):
        self.bot = bot
        with open("locations.json") as f:
            self.room_positions = json.load(f)

    async def execute(self, user: User, args: list, message: str):
        response = await self.bot.highrise.get_room_users()
        users = [content[0] for content in response.content]
        usernames = [user.username.lower() for user in users]

        if len(args) < 2:
            await self.bot.highrise.send_whisper(user.id, "Invalid usage: teleport @username <position> or teleport @username x y z")
            return
        elif args[0][0] != "@":
            await self.bot.highrise.send_whisper(user.id, "Invalid user format")
            return
        elif args[0][1:].lower() not in usernames:
            await self.bot.highrise.send_whisper(user.id, f"Invalid player: {args[0][1:]}")
            return
        elif len(args) == 4:
            try:
                x, y, z = float(args[1]), float(args[2]), float(args[3])
                dest = Position(x, y, z)
            except ValueError:
                await self.bot.highrise.send_whisper(user.id, "Invalid coordinates")
                return
        else:
            position_name = " ".join(args[1:])
            if position_name not in self.room_positions.get("spawn", {}):
                await self.bot.highrise.send_whisper(user.id, f"{position_name} is not a valid position in this room.")
                return
            else:
                dest = Position(*self.room_positions["spawn"][position_name])

        user_id = next(
            (u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
        if not user_id:
            await self.bot.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
            return
        await self.bot.highrise.teleport(user_id, dest)
