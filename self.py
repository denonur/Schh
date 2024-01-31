import subprocess
import time

while True:
    print("Starting bot...")
    bot_process = subprocess.Popen(["python3", "repl_watchdog.py"])
    bot_process.wait()  # Wait for the bot process to finish
    print("Bot stopped. Restarting in 5 seconds...")
    time.sleep(5)  # Wait before restarting