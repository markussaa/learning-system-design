import asyncio
import threading
from flask import Flask, request, jsonify

### === ACTOR SYSTEM === ###
class Actor:
    def __init__(self):
        self.mailbox = asyncio.Queue()
    
    async def send(self, message):
        await self.mailbox.put(message)

    async def run(self):
        raise NotImplementedError()

class LoggerActor(Actor):
    print("[LoggerActor] started", flush=True)
    async def run(self):
        while True:
            message = await self.mailbox.get()
            print(f"[LOG] {message}", flush=True)

class UserActor(Actor):
    print("[UserActor] started", flush=True)
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.valid_users = {123, 456}
        
    async def run(self):
        while True:
            message = await self.mailbox.get()

            user_id = message["user_id"]
            reply_to = message["reply_to"]

            is_valid = user_id in self.valid_users 

            await self.logger.send(f"Checked user {user_id}: {'Valid' if is_valid else 'Invalid'}")

            reply_to.set_result(is_valid)
            

class APIActor(Actor):
    print("[APIActor] started", flush=True)
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
    print("[APIActor] started", flush=True)
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    async def run(self):
        while True:
            message = await self.mailbox.get()

            user_id = message["user_id"]
            amount = message["amount"]

            await self.logger.send(f"Processed payment of {amount} for user={user_id}")

### === ASYNCIO BACKGROUND TASK === ###

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

logger = LoggerActor()
user_actor = UserActor(logger)
payment_actor = PaymentActor(logger)
api_actor = APIActor(logger, user_actor, payment_actor)

tasks = [loop.create_task(actor.run()) for actor in [logger, user_actor, payment_actor, api_actor]]

def run_event_loop():
    loop.run_forever()

threading.Thread(target=run_event_loop, daemon=True).start()

### === FLASK === ###

app = Flask(__name__)

@app.route("/pay", methods=["POST"])
def pay():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    asyncio.run_coroutine_threadsafe(
        api_actor.send({"user_id": user_id, "amount": amount}),
        loop
    )

    return jsonify({"status": "Request accepted"}), 202

if __name__ == "__main__":
    print("Server running on http://127.0.0.1:5001")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)