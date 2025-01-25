from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
db = client['authdb']
subjects_collection = db['subtopics']
user_subtopics_collection = db['user_subtopics']  # New collection for storing user-specific subtopic orders


@app.route('/get_api_key', methods=['POST'])
def get_api_key():
    """Mock endpoint to return API key for a user after login/registration."""
    username = request.json.get("email")
    # Mock logic to get or create an API key for the user
    api_key = f"{username}_api_key"  # Replace with actual logic
    return jsonify({"api_key": api_key})


@app.route('/subtopics', methods=['GET'])
def get_subtopics():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    section = request.args.get('section')
    topic = request.args.get('topic')
    api_key = request.headers.get('API-Key')

    if not (subject and class_name and section and topic and api_key):
        return jsonify({"error": "Subject, class, section, topic, and API-Key are required!"}), 400

    # Check if user-specific order exists
    user_data = user_subtopics_collection.find_one(
        {"api_key": api_key, "subject": subject, "class": class_name, "section": section, "topic": topic},
        {"_id": 0, "subtopics": 1}
    )
    if user_data:
        return jsonify({"subtopics": user_data.get("subtopics", [])}), 200

    # Fallback to default subtopic order
    result = subjects_collection.find_one(
        {"subject": subject, "class": class_name, "section": section, "topics.name": topic},
        {"topics.$": 1, "_id": 0}
    )
    if not result or not result.get('topics'):
        return jsonify({"error": "No subtopics found for the given topic!"}), 404

    subtopics = result['topics'][0].get('subtopics', [])
    return jsonify({"subtopics": subtopics}), 200


@app.route('/reorder_subtopics', methods=['PUT'])
def reorder_subtopics():
    data = request.json
    subject = data.get('subject')
    class_name = data.get('class')
    section = data.get('section')
    topic = data.get('topic')
    new_order = data.get('subtopics')
    api_key = request.headers.get('API-Key')

    if not (subject and class_name and section and topic and new_order and api_key):
        return jsonify({"error": "Subject, class, section, topic, subtopics, and API-Key are required!"}), 400

    # Update or insert user-specific subtopic order
    user_subtopics_collection.update_one(
        {"api_key": api_key, "subject": subject, "class": class_name, "section": section, "topic": topic},
        {"$set": {"subtopics": new_order}},
        upsert=True
    )

    return jsonify({"message": "Subtopics reordered successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True)