# come.py
from highrise import*
from highrise.models import* # Replace 'some_module' with the actual module where Position is defined

async def come_command(user, highrise):
    response = await highrise.get_room_users()
    your_pos = None
    for content in response.content:
        if content[0].id == user.id:
            if isinstance(content[1], Position):
                your_pos = content[1]
                break
    if not your_pos:
        await highrise.send_whisper(user.id, f"You don't have permission to use this command")
        return
    await highrise.chat(f"@{user.username} I'm coming ..")
    await highrise.walk_to(your_pos)
