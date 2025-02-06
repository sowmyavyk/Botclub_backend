from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI", "mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority"))
db = client['authdb']
scheduled_lessons_collection = db['scheduled_lessons']

@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    schedule_id = request.args.get("schedule_id")

    if not schedule_id:
        return jsonify({"error": "schedule_id is required!"}), 400
    
    try:
        schedule_obj_id = ObjectId(schedule_id)
    except:
        return jsonify({"error": "Invalid schedule_id!"}), 400
    
    schedule = scheduled_lessons_collection.find_one({"_id": schedule_obj_id})
    
    if not schedule:
        return jsonify({"error": "Schedule not found!"}), 404

    # Convert `_id` to string
    schedule["_id"] = str(schedule["_id"])

    return jsonify(schedule), 200

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    """Create a new scheduled lesson with updated details."""
    data = request.json
    schedule_id = data.get("schedule_id")

    if not schedule_id:
        return jsonify({"error": "schedule_id is required!"}), 400

    try:
        schedule_obj_id = ObjectId(schedule_id)
    except:
        return jsonify({"error": "Invalid schedule_id!"}), 400

    # Fetch existing schedule
    existing_schedule = scheduled_lessons_collection.find_one({"_id": schedule_obj_id})
    if not existing_schedule:
        return jsonify({"error": "Schedule not found!"}), 404

    # Fetch the API key from the existing schedule
    api_key = existing_schedule.get("api_key")

    # If no API key exists in the original schedule, return an error
    if not api_key:
        return jsonify({"error": "API key missing in the original schedule!"}), 400

    # Prepare new schedule data to check against existing schedules
    new_schedule = {
        "api_key": api_key,  # Include the same API key
        "subject": data.get("subject", existing_schedule.get("subject")),
        "class": data.get("class", existing_schedule.get("class")),
        "section": data.get("section", existing_schedule.get("section")),
        "topic": data.get("topic", existing_schedule.get("topic")),
        "date": data.get("date", existing_schedule.get("date")),
        "time_slot": data.get("time_slot", existing_schedule.get("time_slot")),
        "selected_subtopics": data.get("selected_subtopics", existing_schedule.get("selected_subtopics")),
    }

    # Check if a schedule already exists with the same details, excluding the current schedule
    duplicate_schedule = scheduled_lessons_collection.find_one({
        "api_key": new_schedule["api_key"],
        "subject": new_schedule["subject"],
        "class": new_schedule["class"],
        "section": new_schedule["section"],
        "topic": new_schedule["topic"],
        "date": new_schedule["date"],
        "time_slot": new_schedule["time_slot"],
        "selected_subtopics": new_schedule["selected_subtopics"]
    })

    if duplicate_schedule:
        return jsonify({"message": "No changes detected, nothing to update!"}), 400

    # Insert new schedule with the updated details
    new_schedule_id = scheduled_lessons_collection.insert_one(new_schedule).inserted_id

    return jsonify({"message": "New schedule created successfully!", "new_schedule_id": str(new_schedule_id)}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))