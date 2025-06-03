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

            user_id = message["user_id"]
            reply_to = message["reply_to"]

            await self.logger.send(f"Validated user: {user_id}")

            reply_to.set_result(True)
            

class APIActor(Actor):
    def __init__(self, logger, user_actor, payment_actor):
        super().__init__()
        self.logger = logger
        self.user_actor = user_actor
        self.payment_actor = payment_actor
        
        
    async def run(self):
        while True:
            message = await self.mailbox.get()

            user_id = message["user_id"]
            amount = message["amount"]

            await self.logger.send(f"Recieved API request: user={user_id}, amount={amount}")

            future = asyncio.get_running_loop().create_future()

            await self.user_actor.send({"user_id": user_id, "reply_to": future})

            is_valid = await future

            if is_valid:
                await self.payment_actor.send({"user_id": user_id, "amount": amount, "reply_to": future})
            else: 
                await self.logger.send(f"Payment declined: Invalid user {user_id}")

class PaymentActor(Actor):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    async def run(self):
        while True:
            message = await self.mailbox.get()

            user_id = message["user_id"]
            amount = message["amount"]

            await self.logger.send(f"Processed payment of {amount} for user={user_id}")

async def main():
    logger = LoggerActor()
    user_actor = UserActor(logger)
    payment_actor = PaymentActor(logger)
    api_actor = APIActor(logger, user_actor, payment_actor)

    tasks = [asyncio.create_task(actor.run()) for actor in [logger, user_actor, payment_actor, api_actor]]

    await api_actor.send({"user_id": 123, "amount": 75})
    await api_actor.send({"user_id": 999, "amount": 100})
    

    await asyncio.sleep(1)

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())