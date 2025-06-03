from flask import Flask, request, jsonify

app = Flask(__name__)

valid_users = {123, 456}

def log(message):
    print(f"[log] {message}")

def validate_user(user_id):
    log(f"Validating user {user_id}")

    is_valid = user_id in valid_users

    log(f"User {user_id} is {"valid" if is_valid else "invalid"}")

    return is_valid

def process_payment(user_id, amount):
    log(f"Processing payment of {amount} for user {user_id}")

    log(f"Payment of {amount} for user {user_id} completed")

@app.route("/pay", methods=["POST"])
def pay():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    log(f"Received payment request: user={user_id}, amount={amount}")

    if validate_user(user_id):
        process_payment(user_id, amount)
    else:
        log(f"Payment declined: Invalid user {user_id}")

    return jsonify({"status": "Request accepted"}), 202

if __name__ == "__main__":
    log("Simple server running on http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
