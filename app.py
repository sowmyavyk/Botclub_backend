from flask import Flask, request, jsonify, session, render_template
from pymongo import MongoClient
import jwt
import datetime
import base64
import os
from flask import send_file
import uuid  # To generate unique API keys
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit

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
    """Register a new user and return an API key along with a profile picture URL."""
    if 'profile_picture' not in request.files:
        return jsonify({"error": "Profile picture is required!"}), 400

    data = request.form
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    subject = data.get('subject')
    school_name = data.get('school')
    profile_pic = request.files['profile_picture']

    # Validate required fields
    if not all([name, email, phone, subject, school_name, profile_pic]):
        return jsonify({"error": "All fields are required!"}), 400

    # Check if the school exists
    if not schools_collection.find_one({"name": school_name}):
        return jsonify({"error": "Selected school does not exist!"}), 400

    # Check if the email exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists!"}), 400

    # Secure filename and create unique file path
    filename = secure_filename(profile_pic.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    profile_pic.save(file_path)

    # Generate a publicly accessible URL
    profile_pic_url = request.host_url + f"static/uploads/{unique_filename}"

    # Generate a unique API key
    api_key = str(uuid.uuid4())

    # Store user in the database
    user = {
        "name": name,
        "email": email,
        "phone": phone,
        "subject": subject,
        "school": school_name,
        "api_key": api_key,  # Return API key
        "profile_picture": profile_pic_url,
        "created_at": datetime.datetime.utcnow()
    }

    users_collection.insert_one(user)
    
    return jsonify({
        "message": "User registered successfully!",
        "api_key": api_key,  # Now returning API key
        "profile_picture": profile_pic_url
    }), 201

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

@app.route('/protected', methods=['GET'])
def protected():
    """Access a protected route using JWT token."""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({"message": f"Welcome, {decoded_token['email']}!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

@app.route('/profile', methods=['GET'])
def profile():
    """Retrieve user profile with a Unity-compatible image URL."""
    api_key = request.headers.get('API-Key')

    if not api_key:
        return jsonify({"error": "API Key is missing!"}), 400

    user = users_collection.find_one(
        {"api_key": api_key},
        {"_id": 0, "name": 1, "email": 1, "phone": 1, "subject": 1, "school": 1, "profile_picture": 1}
    )

    if not user:
        return jsonify({"error": "Invalid API Key!"}), 403

    return jsonify({"profile": user}), 200

@app.route("/update_profile", methods=["POST"])
def update_profile():
    """Update the user's profile, allowing changes only for phone and profile picture."""
    api_key = request.headers.get("API-Key")

    if not api_key:
        return jsonify({"error": "API Key is missing!"}), 400

    user = users_collection.find_one({"api_key": api_key})
    if not user:
        return jsonify({"error": "Invalid API Key!"}), 403

    update_data = {}

    # Check request type (JSON or multipart/form-data)
    if request.content_type == "application/json":
        data = request.get_json()
        new_phone = data.get("phone")
        if new_phone:
            update_data["phone"] = new_phone

    elif request.content_type.startswith("multipart/form-data"):
        new_phone = request.form.get("phone")
        profile_pic = request.files.get("profile_picture")

        if new_phone:
            update_data["phone"] = new_phone

        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            profile_pic.save(file_path)

            # Generate public URL for Unity
            profile_pic_url = request.host_url + f"static/uploads/{unique_filename}"
            update_data["profile_picture"] = profile_pic_url

    # If no valid update data was provided
    if not update_data:
        return jsonify({"error": "No valid fields provided to update!"}), 400

    # Apply the update in MongoDB
    users_collection.update_one({"api_key": api_key}, {"$set": update_data})

    return jsonify({"message": "Profile updated successfully!", **update_data}), 200
@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    """Serve the uploaded profile pictures."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned PORT or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
