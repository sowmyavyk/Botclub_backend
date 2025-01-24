from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
db = client['authdb']  # Use 'authdb' as the database
subjects_collection = db['subtopics']  # Collection storing subject, class, section, and topic data

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

# Insert sample data on application startup
insert_sample_data()

@app.route('/')
def home():
    return "API is running."

@app.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = subjects_collection.distinct("subject")
    return jsonify({"subjects": subjects}), 200

@app.route('/classes', methods=['GET'])
def get_classes():
    subject = request.args.get('subject')
    if not subject:
        return jsonify({"error": "Subject is required!"}), 400
    # Fetching classes from the nested structure of the document
    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data:
        classes = list(subject_data["classes"].keys())
        return jsonify({"classes": classes}), 200
    else:
        return jsonify({"error": "Subject not found!"}), 404

@app.route('/sections', methods=['GET'])
def get_sections():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    if not subject or not class_name:
        return jsonify({"error": "Subject and class are required!"}), 400
    # Fetching sections from the nested structure of the document
    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data and class_name in subject_data["classes"]:
        sections = list(subject_data["classes"][class_name]["sections"].keys())
        return jsonify({"sections": sections}), 200
    else:
        return jsonify({"error": "No sections found for the given subject and class!"}), 404

@app.route('/topics', methods=['GET'])
def get_topics():
    subject = request.args.get('subject')
    class_name = request.args.get('class')
    section = request.args.get('section')
    if not subject or not class_name or not section:
        return jsonify({"error": "Subject, class, and section are required!"}), 400
    # Fetching topics from the nested structure of the document
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
    if not subject or not class_name or not section or not topic:
        return jsonify({"error": "Subject, class, section, and topic are required!"}), 400
    # Fetching subtopics from the nested structure of the document
    subject_data = subjects_collection.find_one({"subject": subject})
    if subject_data and class_name in subject_data["classes"]:
        class_data = subject_data["classes"][class_name]
        if section in class_data["sections"]:
            for t in class_data["sections"][section]["topics"]:
                if t["name"] == topic:
                    return jsonify({"subtopics": t["subtopics"]}), 200
    return jsonify({"error": "No subtopics found for the given topic!"}), 404

if __name__ == "__main__":
    # Ensure the app binds to the correct port
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5002)))