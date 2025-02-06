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
    """Fetch schedule details by schedule_id."""
    schedule_id = request.args.get("schedule_id")

    if not schedule_id:
        return jsonify({"error": "schedule_id is required!"}), 400
    
    try:
        schedule_obj_id = ObjectId(schedule_id)
    except:
        return jsonify({"error": "Invalid schedule_id!"}), 400
    
    schedule = scheduled_lessons_collection.find_one({"_id": schedule_obj_id}, {"_id": 0})  # Exclude _id from response

    if not schedule:
        return jsonify({"error": "Schedule not found!"}), 404

    return jsonify(schedule), 200

@app.route('/update_schedule', methods=['PUT'])
def update_schedule():
    """Update an existing scheduled lesson."""
    data = request.json
    schedule_id = data.get("schedule_id")

    if not schedule_id:
        return jsonify({"error": "schedule_id is required!"}), 400

    # Validate ObjectId
    try:
        schedule_obj_id = ObjectId(schedule_id)
    except:
        return jsonify({"error": "Invalid schedule_id!"}), 400

    # Check if schedule exists
    schedule = scheduled_lessons_collection.find_one({"_id": schedule_obj_id})
    if not schedule:
        return jsonify({"error": "Schedule not found!"}), 404

    # Allowed fields for update
    allowed_fields = {"section", "date", "time_slot"}
    update_data = {field: data[field] for field in allowed_fields if field in data}

    if update_data:
        result = scheduled_lessons_collection.update_one(
            {"_id": schedule_obj_id}, 
            {"$set": update_data}
        )
        if result.modified_count > 0:
            return jsonify({"message": "Schedule updated successfully!", "schedule_id": str(schedule_obj_id)}), 200
        else:
            return jsonify({"message": "No changes made to the schedule."}), 200

    return jsonify({"error": "No valid fields provided for update!"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))