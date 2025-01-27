from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority")
db = client['authdb']
subjects_collection = db['subtopics']  # Use the 'subtopics' collection in 'authdb'
user_subtopics_collection = db['user_subtopics']  # Collection for storing user-specific subtopic orders

def insert_sample_data():
    if subjects_collection.count_documents({}) == 0:
        syllabus_data = [
            {
                "subject": "Mathematics",
                "classes": {
                    "8": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Number Systems",
                                        "subtopics": ["Rational Numbers", "Irrational Numbers", "Real Numbers"]
                                    },
                                    {
                                        "name": "Algebra",
                                        "subtopics": ["Linear Equations in One Variable", "Factorization"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Number Systems",
                                        "subtopics": ["Rational Numbers", "Irrational Numbers", "Real Numbers"]
                                    },
                                    {
                                        "name": "Algebra",
                                        "subtopics": ["Linear Equations in One Variable", "Factorization"]
                                    }
                                ]
                            }
                        }
                    },
                    "10": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Trigonometry",
                                        "subtopics": ["Introduction to Trigonometric Ratios", "Trigonometric Identities"]
                                    },
                                    {
                                        "name": "Probability",
                                        "subtopics": ["Experimental Probability", "Theoretical Probability"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Trigonometry",
                                        "subtopics": ["Introduction to Trigonometric Ratios", "Trigonometric Identities"]
                                    },
                                    {
                                        "name": "Probability",
                                        "subtopics": ["Experimental Probability", "Theoretical Probability"]
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
                    "8": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Force and Pressure",
                                        "subtopics": ["Contact Forces", "Pressure in Fluids", "Applications of Pressure"]
                                    },
                                    {
                                        "name": "Friction",
                                        "subtopics": ["Types of Friction", "Effects of Friction", "Reducing Friction"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Force and Pressure",
                                        "subtopics": ["Contact Forces", "Pressure in Fluids", "Applications of Pressure"]
                                    },
                                    {
                                        "name": "Friction",
                                        "subtopics": ["Types of Friction", "Effects of Friction", "Reducing Friction"]
                                    }
                                ]
                            }
                        }
                    },
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
                    },
                    "10": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Electricity",
                                        "subtopics": ["Ohm's Law", "Resistance", "Series and Parallel Circuits"]
                                    },
                                    {
                                        "name": "Magnetic Effects of Current",
                                        "subtopics": ["Magnetic Field", "Electromagnets", "Force on a Current-Carrying Conductor"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Electricity",
                                        "subtopics": ["Ohm's Law", "Resistance", "Series and Parallel Circuits"]
                                    },
                                    {
                                        "name": "Magnetic Effects of Current",
                                        "subtopics": ["Magnetic Field", "Electromagnets", "Force on a Current-Carrying Conductor"]
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            {
                "subject": "Chemistry",
                "classes": {
                    "8": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Materials",
                                        "subtopics": ["Metals", "Non-Metals", "Uses of Metals and Non-Metals"]
                                    },
                                    {
                                        "name": "Combustion and Flame",
                                        "subtopics": ["Combustion", "Flame", "Types of Combustion"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Materials",
                                        "subtopics": ["Metals", "Non-Metals", "Uses of Metals and Non-Metals"]
                                    },
                                    {
                                        "name": "Combustion and Flame",
                                        "subtopics": ["Combustion", "Flame", "Types of Combustion"]
                                    }
                                ]
                            }
                        }
                    },
                    "10": {
                        "sections": {
                            "A": {
                                "topics": [
                                    {
                                        "name": "Chemical Reactions and Equations",
                                        "subtopics": ["Types of Chemical Reactions", "Balancing Chemical Equations"]
                                    },
                                    {
                                        "name": "Periodic Classification of Elements",
                                        "subtopics": ["Mendeleev's Periodic Table", "Modern Periodic Table", "Trends in the Periodic Table"]
                                    }
                                ]
                            },
                            "B": {
                                "topics": [
                                    {
                                        "name": "Chemical Reactions and Equations",
                                        "subtopics": ["Types of Chemical Reactions", "Balancing Chemical Equations"]
                                    },
                                    {
                                        "name": "Periodic Classification of Elements",
                                        "subtopics": ["Mendeleev's Periodic Table", "Modern Periodic Table", "Trends in the Periodic Table"]
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

# Call the function to insert data
# Main script to run
if __name__ == "__main__":
    insert_sample_data()