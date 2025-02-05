from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
db = client["user_auth"]
users_collection = db["users"]

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Middleware for API Key Authentication
def authenticate_api_key():
    api_key = request.headers.get("x-api-key")  # Read API key from headers
    return users_collection.find_one({"api_key": api_key})

# Endpoint to update phone number
@app.route("/update_phone", methods=["POST"])
def update_phone():
    data = request.json
    new_phone = data.get("phone")

    user = authenticate_api_key()
    if not user:
        return jsonify({"error": "Invalid API key"}), 401

    users_collection.update_one({"_id": user["_id"]}, {"$set": {"phone": new_phone}})
    return jsonify({"message": "Phone number updated successfully"})

# Endpoint to upload profile picture
@app.route("/update_profile_picture", methods=["POST"])
def update_profile_picture():
    user = authenticate_api_key()
    if not user:
        return jsonify({"error": "Invalid API key"}), 401

    file = request.files.get("profile_picture")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = f"{user['_id']}_{file.filename}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    users_collection.update_one({"_id": user["_id"]}, {"$set": {"profile_picture": filepath}})
    return jsonify({"message": "Profile picture uploaded successfully", "file_path": filepath})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5002)))