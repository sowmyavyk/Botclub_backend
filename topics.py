from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
db = client['authdb']
subjects_collection = db['subtopics']  # Use the 'subtopics' collection in 'authdb'
user_subtopics_collection = db['user_subtopics']  # Collection for storing user-specific subtopic orders
@app.route('/')
def home():
    return "API is running!"

@app.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = subjects_collection.distinct("subject")
    return jsonify({"subjects": subjects}), 200

@app.route('/classes', methods=['GET'])
def get_classes():
    subject = request.args.get('subject')
    if not subject:
        return jsonify({"error": "Subject is required!"}), 400
    
    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data:
        classes = list(subject_data.get("classes", {}).keys())
        return jsonify({"classes": classes}), 200
    return jsonify({"error": "Subject not found!"}), 404

@app.route('/sections', methods=['GET'])
def get_sections():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    if not subject or not class_name:
        return jsonify({"error": "Subject and class are required!"}), 400

    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data:
        class_data = subject_data.get("classes", {}).get(class_name, {})
        if "sections" in class_data:
            sections = list(class_data["sections"].keys())
            return jsonify({"sections": sections}), 200
    return jsonify({"error": "No sections found for the given subject and class!"}), 404

@app.route('/topics', methods=['GET'])
def get_topics():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    section = request.args.get('section')
    if not subject or not class_name or not section:
        return jsonify({"error": "Subject, class, and section are required!"}), 400

    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data:
        class_data = subject_data.get("classes", {}).get(class_name, {})
        section_data = class_data.get("sections", {}).get(section, {})
        if "topics" in section_data:
            topics = [topic["name"] for topic in section_data["topics"]]
            return jsonify({"topics": topics}), 200
    return jsonify({"error": "No topics found for the given criteria!"}), 404

@app.route('/subtopics', methods=['GET'])
def get_subtopics():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    section = request.args.get('section')
    topic = request.args.get('topic')
    api_key = request.headers.get('API-Key')

    if not (subject and class_name and section and topic and api_key):
        return jsonify({"error": "Subject, class, section, topic, and API-Key are required!"}), 400

    # Check for user-specific subtopic order
    user_data = user_subtopics_collection.find_one(
        {"api_key": api_key, "subject": subject, "class": class_name, "section": section, "topic": topic},
        {"_id": 0, "subtopics": 1}
    )
    if user_data and user_data.get("subtopics"):
        return jsonify({"subtopics": user_data["subtopics"]}), 200

    # Default subtopic order
    subject_data = subjects_collection.find_one(
        {"subject": subject},
        {"classes." + class_name + ".sections." + section + ".topics": 1, "_id": 0}
    )
    if not subject_data:
        return jsonify({"error": "No subtopics found for the given topic!"}), 404

    class_data = subject_data["classes"].get(class_name, {})
    section_data = class_data.get("sections", {}).get(section, {})
    topics = section_data.get("topics", [])

    for t in topics:
        if t["name"] == topic:
            return jsonify({"subtopics": t["subtopics"]}), 200

    return jsonify({"error": "No subtopics found for the given topic!"}), 404

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

    user_subtopics_collection.update_one(
        {"api_key": api_key, "subject": subject, "class": class_name, "section": section, "topic": topic},
        {"$set": {"subtopics": new_order}},
        upsert=True
    )

    return jsonify({"message": "Subtopics reordered successfully!"}), 200

@app.route('/get_api_key', methods=['POST'])
def get_api_key():
    username = request.json.get("email")
    api_key = f"{username}_api_key"
    return jsonify({"api_key": api_key})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))