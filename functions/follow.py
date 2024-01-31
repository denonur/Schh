from highrise import *
from highrise.models import *
import asyncio

async def follow(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            await self.highrise.chat("Already following someone")
            return
    # Checks if this function is already in the Highrise class tg (task group).
    taskgroup.create_task(coro=following_loop(self, user, message), name="following_loop")
    await self.highrise.chat(f"Following {user.username}")

async def following_loop(self: BaseBot, user: User, message: str) -> None:
    if message.startswith("/following_loop"):
        await self.highrise.chat("Invalid command, please use /follow")
        return
    while True:
        # Gets the user position
        room_users = (await self.highrise.get_room_users()).content
        for room_user, position in room_users:
            if room_user.id == user.id:
                user_position = position
                break
        print(user_position)
        if type(user_position) != AnchorPosition:
            await self.highrise.walk_to(Position(user_position.x + 1, user_position.y, user_position.z))
        await asyncio.sleep(0.5)

async def stop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            task.cancel()
            await self.highrise.chat(f"Stopping following {user.username}")
            return
    await self.highrise.chat("Not following anyone")

