import time

async def ping_handler(highrise):
    start_time = time.time()
    try:
        response = await highrise.chat("Pong!")
    except Exception as e:
        print(f"Error: {e}")
    else:
        end_time = time.time()
        ping = (end_time - start_time) * 1000  # Convert to milliseconds
        await highrise.chat(f"Bot's Ping: {ping:.2f} ms")
        return response