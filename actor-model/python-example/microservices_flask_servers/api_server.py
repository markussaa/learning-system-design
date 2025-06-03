from flask import Flask, request 
import requests

app = Flask(__name__)

def validate_user(user_id):
    response = requests.post("http://localhost:5002/validate-user", json={"user_id": user_id})

    if response.status_code != 200:
        return False

    return True 

def process_payment(user_id, amount):
    requests.post("http://localhost:5003/make-payment", json={"user_id": user_id, "amount": amount})

@app.route('/pay', methods=["POST"])
def make_payment():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    print(f"Recieved payment request: user={user_id}, amount={amount}")

    if (validate_user(user_id)):
        print(f"User {user_id} was valid")

        process_payment(user_id, amount)
        
        print(f"Payment processed for user {user_id}")

        return "Successfully processed payment", 200

    else:
        print(f"User {user_id} was not valid")
        return "Invalid User", 400
    


if __name__ == "__main__":
    print("Payment server was started on http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)