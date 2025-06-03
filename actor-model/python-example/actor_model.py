import asyncio

class Actor:
    def __init__(self):
        self.mailbox = asyncio.Queue()
    
    async def send(self, message):
        await self.mailbox.put(message)
        print(self.mailbox)

    async def run(self):
        raise NotImplementedError()

class LoggerActor(Actor):
    async def run(self):
        while True:
            message = await self.mailbox.get()
            print(f"[LOG] {message}")

class UserActor(Actor):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        
    async def run(self):
        while True:
            message = await self.mailbox.get()
            print(f"[LOG] {message}")

class APIActor(Actor):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        
    async def run(self):
        while True:
            message = await self.mailbox.get()
            print(f"[LOG] {message}")

class PaymentActor(Actor):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        
    async def run(self):
        while True:
            message = await self.mailbox.get()
            print(f"[LOG] {message}")

async def main():
    logger = LoggerActor()

    tasks = [asyncio.create_task(actor.run()) for actor in [logger]]

    await logger.send("Hello world")

    await asyncio.sleep(1)

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())