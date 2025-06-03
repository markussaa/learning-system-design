from locust import HttpUser, task, between
import random
import json

class PaymentUser(HttpUser):
    wait_time = between(1, 3)  # Simulates a wait between tasks

    @task
    def make_payment(self):
        user_id = random.choice([123, 456, 789, 111, 222])  # Some valid/invalid users
        amount = random.randint(10, 100)

        payload = {
            "user_id": user_id,
            "amount": amount
        }

        self.client.post(
            "/pay",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
