# reactions.py
import asyncio
from highrise import*
from highrise.models import*

async def send_reaction(user, highrise, reaction_type, count):
    try:
        count = int(count)
        if count <= 0:
            await highrise.chat("Please enter a valid number greater than 0.")
            return

        for _ in range(count):
            await highrise.react(reaction_type, user.id)
            await asyncio.sleep(0.1)  # Adjust the delay duration if needed

    except ValueError:
        await highrise.chat(f"Please enter a valid number after {reaction_type}.")
