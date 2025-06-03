import asyncio

class Actor:
    def __init__(self):
        self.mailbox = asyncio.Queue()
    
    async def send(self, message):
        await self.mailbox.put(message)

    async def run(self):
        raise NotImplementedError()


async def main():
    actor = Actor()

    await actor.send("Hello World")

asyncio.run(main())