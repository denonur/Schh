from highrise.models import*
from highrise.models import*

class SayCommand:
    def __init__(self, bot):
        self.bot = bot
        self.name = "say"
        self.cooldown = 1

    async def execute(self, user: User, args: list, message: str):
        if message.startswith("say"):
            text = message.replace("say", "").strip()
            await self.bot.highrise.chat(text)
