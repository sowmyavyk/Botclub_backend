from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
db = client['authdb']
subjects_collection = db['subtopics']
user_subtopics_collection = db['user_subtopics']  # Collection for storing user-specific subtopic orders


# Function to insert sample data if it doesn't exist
def insert_sample_data():
    if subjects_collection.count_documents({}) == 0:
        syllabus_data = [
            {
                "subject": "Mathematics",
                "classes": {
                    "10": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Algebra",
                                        "subtopics": ["Linear Equations", "Quadratic Equations", "Polynomials"]
                                    },
                                    {
                                        "name": "Geometry",
                                        "subtopics": ["Triangles", "Circles", "Coordinate Geometry"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Algebra",
                                        "subtopics": ["Linear Equations", "Quadratic Equations", "Polynomials"]
                                    },
                                    {
                                        "name": "Geometry",
                                        "subtopics": ["Triangles", "Circles", "Coordinate Geometry"]
                                    }
                                ]
                            },
                            "C": {
                                "topics": [
                                    {
                                        "name": "Algebra",
                                        "subtopics": ["Linear Equations", "Quadratic Equations", "Polynomials"]
                                    },
                                    {
                                        "name": "Geometry",
                                        "subtopics": ["Triangles", "Circles", "Coordinate Geometry"]
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            {
                "subject": "Physics",
                "classes": {
                    "9": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Light - Reflection and Refraction",
                                        "subtopics": [
                                            "Specular Reflection - Smooth Reflection",
                                            "Rough Reflection",
                                            "Visible Light",
                                            "Properties of visible light",
                                            "Reflection of light from mirror",
                                            "Transparent objects",
                                            "Translucent objects",
                                            "Opaque objects",
                                            "Laws of Reflection - First Law",
                                            "Second Law",
                                            "Third Law",
                                            "Experimental Model working",
                                            "Total internal reflection of light"
                                        ]
                                    },
                                    {
                                        "name": "Force and Pressure",
                                        "subtopics": [
                                            "Atmospheric Pressure (Properties)",
                                            "Vacuum",
                                            "Difference in pressure conditions",
                                            "Processes in Earth's atmosphere and Vacuum",
                                            "Measuring Atmospheric Pressure - Barometer Example A",
                                            "Barometer Example B",
                                            "Barometer Example C",
                                            "Application - Vacuum Pump",
                                            "Force caused by atmospheric pressure",
                                            "Difference between air pressure and vacuum",
                                            "Experimental Model working"
                                        ]
                                    },
                                    {
                                        "name": "Motion and Time",
                                        "subtopics": [
                                            "Measurement of Time",
                                            "Motion along a straight line",
                                            "Uniform motion",
                                            "Non-uniform motion",
                                            "Measuring distance",
                                            "Displacement - Example 1",
                                            "Displacement - Example 2",
                                            "Distance-Time Graph",
                                            "Speed with direction",
                                            "Rate of change of velocity",
                                            "Difference between speed and velocity",
                                            "Oscillatory motion of a pendulum",
                                            "Measurement of time using oscillations of a pendulum",
                                            "Time period of a pendulum",
                                            "Magnetic field due to a current through a circular loop",
                                            "Experimental Model working"
                                        ]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Light - Reflection and Refraction",
                                        "subtopics": [
                                            "Specular Reflection - Smooth Reflection",
                                            "Rough Reflection",
                                            "Visible Light",
                                            "Properties of visible light",
                                            "Reflection of light from mirror",
                                            "Transparent objects",
                                            "Translucent objects",
                                            "Opaque objects",
                                            "Laws of Reflection - First Law",
                                            "Second Law",
                                            "Third Law",
                                            "Experimental Model working",
                                            "Total internal reflection of light"
                                        ]
                                    },
                                    {
                                        "name": "Force and Pressure",
                                        "subtopics": [
                                            "Atmospheric Pressure (Properties)",
                                            "Vacuum",
                                            "Difference in pressure conditions",
                                            "Processes in Earth's atmosphere and Vacuum",
                                            "Measuring Atmospheric Pressure - Barometer Example A",
                                            "Barometer Example B",
                                            "Barometer Example C",
                                            "Application - Vacuum Pump",
                                            "Force caused by atmospheric pressure",
                                            "Difference between air pressure and vacuum",
                                            "Experimental Model working"
                                        ]
                                    },
                                    {
                                        "name": "Motion and Time",
                                        "subtopics": [
                                            "Measurement of Time",
                                            "Motion along a straight line",
                                            "Uniform motion",
                                            "Non-uniform motion",
                                            "Measuring distance",
                                            "Displacement - Example 1",
                                            "Displacement - Example 2",
                                            "Distance-Time Graph",
                                            "Speed with direction",
                                            "Rate of change of velocity",
                                            "Difference between speed and velocity",
                                            "Oscillatory motion of a pendulum",
                                            "Measurement of time using oscillations of a pendulum",
                                            "Time period of a pendulum",
                                            "Magnetic field due to a current through a circular loop",
                                            "Experimental Model working"
                                        ]
                                    }
                                ]
                            },
                            "C": {
                                "topics": [
                                    {
                                        "name": "Light - Reflection and Refraction",
                                        "subtopics": [
                                            "Specular Reflection - Smooth Reflection",
                                            "Rough Reflection",
                                            "Visible Light",
                                            "Properties of visible light",
                                            "Reflection of light from mirror",
                                            "Transparent objects",
                                            "Translucent objects",
                                            "Opaque objects",
                                            "Laws of Reflection - First Law",
                                            "Second Law",
                                            "Third Law",
                                            "Experimental Model working",
                                            "Total internal reflection of light"
                                        ]
                                    },
                                    {
                                        "name": "Force and Pressure",
                                        "subtopics": [
                                            "Atmospheric Pressure (Properties)",
                                            "Vacuum",
                                            "Difference in pressure conditions",
                                            "Processes in Earth's atmosphere and Vacuum",
                                            "Measuring Atmospheric Pressure - Barometer Example A",
                                            "Barometer Example B",
                                            "Barometer Example C",
                                            "Application - Vacuum Pump",
                                            "Force caused by atmospheric pressure",
                                            "Difference between air pressure and vacuum",
                                            "Experimental Model working"
                                        ]
                                    },
                                    {
                                        "name": "Motion and Time",
                                        "subtopics": [
                                            "Measurement of Time",
                                            "Motion along a straight line",
                                            "Uniform motion",
                                            "Non-uniform motion",
                                            "Measuring distance",
                                            "Displacement - Example 1",
                                            "Displacement - Example 2",
                                            "Distance-Time Graph",
                                            "Speed with direction",
                                            "Rate of change of velocity",
                                            "Difference between speed and velocity",
                                            "Oscillatory motion of a pendulum",
                                            "Measurement of time using oscillations of a pendulum",
                                            "Time period of a pendulum",
                                            "Magnetic field due to a current through a circular loop",
                                            "Experimental Model working"
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        ]
        subjects_collection.insert_many(syllabus_data)
        print("Sample data inserted into the database.")


insert_sample_data()


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
        classes = list(subject_data["classes"].keys())
        return jsonify({"classes": classes}), 200
    return jsonify({"error": "Subject not found!"}), 404


@app.route('/sections', methods=['GET'])
def get_sections():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    if not subject or not class_name:
        return jsonify({"error": "Subject and class are required!"}), 400
    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data and class_name in subject_data["classes"]:
        sections = list(subject_data["classes"][class_name]["sections"].keys())
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
    if subject_data and class_name in subject_data["classes"]:
        class_data = subject_data["classes"][class_name]
        if section in class_data["sections"]:
            topics = [topic['name'] for topic in class_data["sections"][section]["topics"]]
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