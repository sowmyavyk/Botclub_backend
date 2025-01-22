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

# Profile endpoint
@app.route('/profile', methods=['GET'])
def profile():
    # Extract the token from the Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        # Decode the token
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['username']

        # Fetch user data from MongoDB
        user = users_collection.find_one({"username": username}, {"_id": 0, "password": 0})
        if not user:
            return jsonify({"error": "User not found!"}), 404

        # Return the user's profile
        return jsonify({"profile": user}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))