from flask import Flask, request, jsonify, session
from pymongo import MongoClient
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/user_auth?retryWrites=true&w=majority")
db = client['user_auth']
users_collection = db['users']

# Enable session management
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')

    if not email_or_phone or not password:
        return jsonify({"error": "Email/Phone and password are required!"}), 400

    # Find the user by email or phone in the database
    user = users_collection.find_one({"$or": [{"email": email_or_phone}, {"phone": email_or_phone}]})
    if not user or user.get('password') != password:  # Replace with password hashing in production
        return jsonify({"error": "Invalid email/phone or password!"}), 401

    # Store user info in session
    session['email_or_phone'] = email_or_phone
    return jsonify({"message": "Login successful!"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not email or not phone or not password:
        return jsonify({"error": "Email, phone, and password are required!"}), 400

    # Check if the email or phone already exists
    if users_collection.find_one({"$or": [{"email": email}, {"phone": phone}]}):
        return jsonify({"error": "Email or phone already exists!"}), 400

    # Create a new user
    users_collection.insert_one({"email": email, "phone": phone, "password": password})  # Replace with password hashing in production

    # Automatically log in the user after registration
    session['email_or_phone'] = email  # Store email in session
    return jsonify({"message": "User registered and logged in successfully!"}), 201


@app.route('/profile', methods=['GET'])
def profile():
    # Check if the user is logged in
    if 'email_or_phone' not in session:
        return jsonify({"error": "You are not logged in!"}), 401

    email_or_phone = session['email_or_phone']

    # Fetch user data from MongoDB
    user = users_collection.find_one({"$or": [{"email": email_or_phone}, {"phone": email_or_phone}]}, {"_id": 0, "password": 0})
    if not user:
        return jsonify({"error": "User not found!"}), 404

    # Return the user's profile
    return jsonify({"profile": user}), 200


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))