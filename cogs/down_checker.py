import interactions
import asyncio
import time

class DownChecker(interactions.Extension):
    def __init__(self, bot):
        self.bot: interactions.Client = bot
        asyncio.get_event_loop().create_task(self.run())

    async def run(self):
            while True:
                await self.check_status()
                await asyncio.sleep(5*60)

    async def check_status(self):
        print(f"Checking bot status... at {time.strftime('%m-%d-%Y %H:%M:%S')}")
        with open("bot.log") as f:
            if "The client was unable to send a heartbeat, closing the connection." in f.read():
                print("Bot needs to be restarted")
                open("bot.log", "w").write("")

def setup(bot):
    DownChecker(bot)
