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
            await self.logger.send(message)

class APIActor(Actor):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        
    async def run(self):
        while True:
            message = await self.mailbox.get()
            await self.logger.send(message)

class PaymentActor(Actor):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        
    async def run(self):
        while True:
            message = await self.mailbox.get()
            await self.logger.send(message)

async def main():
    logger = LoggerActor()
    user_actor = UserActor(logger)
    payment_actor = PaymentActor(logger)
    api_actor = APIActor(logger)

    tasks = [asyncio.create_task(actor.run()) for actor in [logger, user_actor, payment_actor, api_actor]]

    await user_actor.send("User")
    await payment_actor.send("Payment")
    await api_actor.send("API")
    

    await asyncio.sleep(1)

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())