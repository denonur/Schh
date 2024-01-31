# print.py
from highrise import*
from highrise.models import*
from highrise.webapi import*
from highrise.models_webapi import*

async def print_user_position(bot, user, args):
    # Get the room users
    response = await bot.highrise.get_room_users()
    users = [content[0] for content in response.content]  # Extract the User objects
    # Extract the usernames in lowercase
    usernames = [user.username.lower() for user in users]

    # Check if the specified user is in the room
    if len(args) != 1:
        await bot.highrise.send_whisper(user.id, "Invalid usage. Please use: /print @username")
        return
    # Check if the lowercase version of the username is in the list
    elif args[0].startswith("@") and len(args[0]) > 1:
        # extract the username by removing the "@" symbol
        username = args[0][1:]
    else:
        username = args[0]
    if username.lower() not in usernames:
        await bot.highrise.send_whisper(user.id, "User not found. Please specify a valid user.")
        return

    # Get the position of the specified user
    # Find the User object for the specified username
    user = users[usernames.index(username.lower())]
    position = None
    for content in response.content:
        if content[0].id == user.id:
            if isinstance(content[1], Position):
                position = content[1]
                msg = f"@{user.username} is at ({position.x}x, {position.y}y, {position.z}z) facing '{position.facing}'"
            elif isinstance(content[1], AnchorPosition):
                position = content[1]
                msg = f"@{user.username} is on entity: {position.entity_id} anchor: {position.anchor_ix}"
            break

    # Print the user ID and position
    print(msg)
    await bot.highrise.chat(msg)
