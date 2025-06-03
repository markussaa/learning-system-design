from flask import Flask, request 

app = Flask(__name__)

@app.route('/make-payment', methods=["POST"])
def make_payment():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    print(f"Recieved payment request: user={user_id}, amount={amount}")

    return "Payment was successfull", 200

if __name__ == "__main__":
    print("Payment server was started on http://localhost:5003")
    app.run(host="0.0.0.0", port=5003, debug=True, use_reloader=False)