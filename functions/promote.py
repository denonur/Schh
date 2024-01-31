from highrise import*
from highrise.models import*
from highrise.webapi import*
from highrise.models_webapi import*

async def promote_user(bot_instance, message, user):
    if user.username not in bot_instance.allowed_usernames:
        await bot_instance.highrise.chat("You do not have permission to use this command.")
        return

    parts = message.split()

    if len(parts) != 3:
        await bot_instance.highrise.chat("Invalid promote command format.")
        return

    command, username, role = parts

    if "@" in username:
        username = username[1:]

    if role.lower() not in ["moderator", "designer"]:
        await bot_instance.highrise.chat("Invalid role, please specify a valid role.")
        return

    # Check if user is in the room
    room_users = (await bot_instance.highrise.get_room_users()).content
    for room_user, pos in room_users:
        if room_user.username.lower() == username.lower():
            user_id = room_user.id
            break
    else:
        await bot_instance.highrise.chat("User not found, please specify a valid user.")
        return

    # Promote user
    try:
        permissions = (await bot_instance.highrise.get_room_privilege(user_id))
        setattr(permissions, role.lower(), True)
        await bot_instance.highrise.change_room_privilege(user_id, permissions)
        await bot_instance.highrise.chat(f"{username} has been promoted to {role}.")
    except Exception as e:
        await bot_instance.highrise.chat(f"Error: {e}")
        return
