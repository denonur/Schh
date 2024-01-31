import time
from highrise import User

async def uptime_command(bot_instance, user, message):
    current_time = time.time()
    uptime_seconds = int(current_time - bot_instance.start_time)
    
    uptime_days = uptime_seconds // 86400
    uptime_seconds %= 86400
    
    uptime_hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    
    uptime_minutes = uptime_seconds // 60
    uptime_seconds %= 60
    
    uptime_formatted = f"{uptime_days} days, {uptime_hours} hours, {uptime_minutes} minutes, {uptime_seconds} seconds"
    
    await bot_instance.highrise.chat(f"Uptime: {uptime_formatted}")

# Assuming you have the rest of your code that initializes the bot and handles events

