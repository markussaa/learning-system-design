from flask import Flask, request 

valid_users = {123, 456}

app = Flask(__name__)

@app.route('/validate-user', methods=["POST"])
def validate_user():
    data = request.json
    user_id = data.get("user_id")

    if user_id not in valid_users:
        print(f"User was not valid, user={user_id}")
        return "User was not valid", 404

    print(f"User was valid, user={user_id}")
    return "User was valid", 200

if __name__ == "__main__":
    print("User server was started on http://localhost:5002")
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)