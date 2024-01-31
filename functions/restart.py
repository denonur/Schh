import os
import sys
from highrise import User

class RestartCommand:
    def __init__(self, bot):
        self.bot = bot
        self.name = "restart"
        self.description = "Restart the bot"
        self.permissions = ["restart"]
        self.cooldown = 1

    async def execute(self, user: User, args: list, message: str):
        await self.bot.highrise.send_whisper(user.id, "Restarting the bot...")
        await self.bot.highrise.logout()
        await self.bot.highrise.close()

        # Restart the bot
        python_executable = sys.executable
        os.execl(python_executable, python_executable, *sys.argv)
