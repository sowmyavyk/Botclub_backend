from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/user_auth?retryWrites=true&w=majority")
db = client["user_auth"]  # Replace with your database name
collection = db["users"]  # Replace with your collection name

@app.route("/get-username", methods=["GET"])
def get_username():
    # Verify API key from the database
    api_key = request.headers.get("API-Key")
    if not api_key:
        return jsonify({"error": "API Key is required"}), 400

    # Fetch user details based on the API key
    user = collection.find_one({"api_key": api_key})  # Ensure API key field exists in the database
    if not user:
        return jsonify({"error": "Unauthorized access"}), 401

    # Extract the username from the user document
    username = user.get("name")
    if not username:
        return jsonify({"error": "Username not found"}), 404

    # Determine greeting based on current time
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return jsonify({
        "message": f"{greeting}, {username}!",
        "username": username
    })

if __name__ == "__main__":
    # Ensure the app binds to the correct port
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5002)))