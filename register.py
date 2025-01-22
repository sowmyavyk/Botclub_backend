from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import jwt
import datetime
import os
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
auth_db = client['user_auth']
users_collection = auth_db['users']
schools_collection = auth_db["schools"] 

# Directory to temporarily store uploaded images (optional, only for processing)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/schools', methods=['GET'])
def get_schools():
    """Fetch and return the list of schools."""
    schools = list(schools_collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field
    return jsonify(schools)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    school_name = request.form.get('school')
    photo = request.files.get('photo')  # The uploaded photo file

    if not all([username, password, email, full_name, phone, school_name, photo]):
        return jsonify({"error": "All fields (username, password, email, full_name, phone, school, photo) are required!"}), 400

    # Check if the school exists in the database
    if not schools_collection.find_one({"name": school_name}):
        return jsonify({"error": "Selected school does not exist!"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists!"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists!"}), 400

    # Save the photo file temporarily and encode it
    filename = secure_filename(photo.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(file_path)

    with open(file_path, "rb") as image_file:
        encoded_photo = base64.b64encode(image_file.read()).decode('utf-8')  # Convert to Base64 string

    # Remove the temporary file
    os.remove(file_path)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "school": school_name,
        "photo": encoded_photo,  # Store the Base64 encoded photo in the database
        "created_at": datetime.datetime.utcnow()
    }

    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully!"}), 201

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
    
@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')  # JWT token from the request header
    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        # Decode the token to extract the username
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['username']

        # Fetch the user details from the database
        user = users_collection.find_one({"username": username}, {"_id": 0, "password": 0})  # Exclude `_id` and `password`

        if not user:
            return jsonify({"error": "User not found!"}), 404

        return jsonify(user), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

if __name__ == "__main__":
    # Ensure the app binds to the correct port
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5002)))