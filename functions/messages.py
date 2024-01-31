import asyncio
import curses
import random
from highrise import BaseBot
from highrise.models import SessionMetadata, User


async def delayed_message_command(self, command: str):
        try:
            _, delay_str, *message_parts = command.split()
            delay = int(delay_str)
            message = " ".join(message_parts)

            await self.highrise.chat(f"Bot will send '{message}' every {delay} seconds.")

            # Start the delayed message loop as a background task
            self.stop_delayed_messages_received = False
            self.bot_loop_task = asyncio.create_task(self.delayed_message_loop(delay, message))
        except ValueError:
            await self.highrise.chat("Invalid command. Usage: delayed_message <delay_seconds> <message>")
        except Exception as e:
            await self.highrise.chat(f"An error occurred: {str(e)}")

async def delayed_message_loop(self, delay: int, message: str):
        while not self.stop_delayed_messages_received:
            await asyncio.sleep(delay)
            await self.highrise.chat(message)

async def stop_delayed_messages(self):
        # Stop the delayed message loop
        self.stop_delayed_messages_received = True
        await self.bot_loop_task  # Wait for the loop task to complete
        await self.highrise.chat("Delayed messages have been stopped.")