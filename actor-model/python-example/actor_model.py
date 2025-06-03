import asyncio

class Actor:
    def __init__(self):
        pass
    
    async def send(self, message):
        print(message)

    async def run(self):
        raise NotImplementedError()


async def main():
    actor = Actor()

    await actor.send("Hello World")

asyncio.run(main())