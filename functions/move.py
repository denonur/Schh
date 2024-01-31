async def move_user(bot_instance, message, user):
    if user.username in bot_instance.allowed_usernames:
        parts = message.split()

        if len(parts) != 3:
            await bot_instance.highrise.chat("Invalid move command format.")
            return

        _, username, room = parts

        if "@" in username:
            username = username[1:]

        if room not in bot_instance.room_dictionary:
            await bot_instance.highrise.chat("Invalid room, please specify a valid room.")
            return

        room_id = bot_instance.room_dictionary[room]  # Get the room ID from the room_dictionary

        # Check if user is in the room
        room_users = (await bot_instance.highrise.get_room_users()).content
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                user_id = room_user.id
                break
        else:
            await bot_instance.highrise.chat("User not found, please specify a valid user.")
            return

        # Move user
        try:
            await bot_instance.highrise.move_user_to_room(user_id, room_id)
            await bot_instance.highrise.chat(f"{username} has been moved to {room}.")
        except Exception as e:
            await bot_instance.highrise.chat(f"Error: {e}")
            return
