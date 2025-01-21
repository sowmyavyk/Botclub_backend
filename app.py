from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import jwt
import datetime
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/user_auth?retryWrites=true&w=majority")
db = client['user_auth']
users_collection = db['users']
schools_collection = db['schools']  # New collection for schools

# Endpoint to fetch school names
@app.route('/schools', methods=['GET'])
def get_schools():
    schools = schools_collection.find({}, {"_id": 0, "name": 1})  # Fetch only the school names
    school_list = [school['name'] for school in schools]
    return jsonify({"schools": school_list}), 200

# Registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    full_name = data.get('full_name')
    phone = data.get('phone')
    school_name = data.get('school_name')

    if not all([username, password, email, full_name, phone, school_name]):
        return jsonify({"error": "All fields (username, password, email, full_name, phone, school_name) are required!"}), 400

    if not schools_collection.find_one({"name": school_name}):
        return jsonify({"error": "Invalid school name!"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists!"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists!"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "school_name": school_name,
        "created_at": datetime.datetime.utcnow()
    }

    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully!"}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    user = users_collection.find_one({"username": username})

    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid username or password!"}), 401

    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"token": token}), 200

# Protected route
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({"message": f"Welcome, {decoded_token['username']}!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

if __name__ == "__main__":
    # Ensure the app binds to the correct port
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
