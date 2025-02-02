from flask import Flask, request, jsonify, session
from pymongo import MongoClient
import jwt
import datetime
import os
import uuid  # To generate unique API keys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
auth_db = client['user_auth']
users_collection = auth_db['users']
schools_collection = auth_db["schools"]

@app.route('/schools', methods=['GET'])
def get_schools():
    """Fetch and return the list of schools."""
    schools = list(schools_collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field
    return jsonify(schools)

@app.route('/register', methods=['POST'])
def register():
    """Register a new user and generate an API key."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    subject = data.get('subject')
    school_name = data.get('school')

    if not all([name, email, phone, subject, school_name]):
        return jsonify({"error": "All fields (name, email, phone, subject, school) are required!"}), 400

    # Check if the school exists in the database
    if not schools_collection.find_one({"name": school_name}):
        return jsonify({"error": "Selected school does not exist!"}), 400

    # Check if the email already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists!"}), 400

    # Generate a unique API key
    api_key = str(uuid.uuid4())

    # Store user in the database
    user = {
        "name": name,
        "email": email,
        "phone": phone,
        "subject": subject,
        "school": school_name,
        "api_key": api_key,  # Save API key
        "created_at": datetime.datetime.utcnow()
    }

    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully!", "api_key": api_key}), 201

@app.route('/login', methods=['POST'])
def login():
    """Authenticate the user and return their API key."""
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')  # Use phone as password

    if not email or not phone:
        return jsonify({"error": "Email and phone number are required!"}), 400

    user = users_collection.find_one({"email": email})

    if not user or user['phone'] != phone:  # Match phone number instead of password
        return jsonify({"error": "Invalid email or phone number!"}), 401

    # Return the user's API key
    return jsonify({"message": "Login successful!", "api_key": user['api_key']}), 200

@app.route('/profile', methods=['GET'])
def profile():
    # Check if the user is logged in via session or token
    token = request.headers.get('Authorization')  # Check for token if no session
    email = session.get('username')  # Session key 'username' stores email after login
    
    if not email and not token:
        return jsonify({"error": "You are not logged in!"}), 401

    # If token exists, decode it and fetch email
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            email = decoded_token.get('email')
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

    # Fetch user data from MongoDB
    user = users_collection.find_one({"email": email}, {"_id": 0, "phone": 1, "name": 1, "subject": 1, "school": 1})
    if not user:
        return jsonify({"error": "User not found!"}), 404

    # Return the user's profile
    return jsonify({"profile": user}), 200

if __name__ == "__main__":
    # Ensure the app binds to the correct port
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5002)))