import os
import time
import subprocess

bot_command = "python3 run.py"  # Replace with the actual command to run your bot

while True:
    try:
        bot_process = subprocess.Popen(bot_command, shell=True)
        bot_process.wait()
        print("Bot process exited. Restarting in 5 seconds...")
        time.sleep(5)
    except KeyboardInterrupt:
        print("Watchdog script interrupted. Exiting...")
        break
