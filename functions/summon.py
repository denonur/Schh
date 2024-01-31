from highrise.models import User, Position


async def summon(bot, user: User, target_username: str):
    # Get the room users
        response = await bot.highrise.get_room_users()
        users = [content[0] for content in response.content]
        usernames = [user.username.lower() for user in users]

    # Check if the specified user is in the room
        if target_username.lower() not in usernames:
            await bot.highrise.send_whisper(user.id, f"User not found. Please specify a valid user.")
            return

    # Get the user ID of the specified user
        target_user = next(user for user in users if user.username.lower() == target_username.lower())
        target_user_id = target_user.id

    # Get the position of the user who issued the command
        summoner_position = None
        for content in response.content:
            if content[0].id == user.id:
                summoner_position = content[1]
                break

        if not summoner_position:
            await bot.highrise.send_whisper(user.id, f"Your position is not available.")
            return

    # Teleport the target user to the position of the summoner
        await bot.highrise.teleport(user_id=target_user_id, dest=summoner_position)

        await bot.highrise.chat(f"{target_user.username} has been summoned to your location.")