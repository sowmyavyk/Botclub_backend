from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
import gridfs
import io

app = Flask(__name__)

# MongoDB Connection (Replace with your MongoDB Atlas URI)
MONGO_URI = "mongodb+srv://Harsha1234:Harsha1234@cluster1.nwz3t.mongodb.net/authdb?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["image_database"]
fs = gridfs.GridFS(db)
api_keys_collection = db["api_keys"]  # Collection to map API keys to images

# Maximum file size (2MB)
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB in bytes
MAX_IMAGES_PER_KEY = 1  # Max images per API key

# Upload Image
@app.route('/upload', methods=['POST'])
def upload_image():
    api_key = request.headers.get("API-Key")
    if not api_key:
        return jsonify({"error": "API key required"}), 400

    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]

    # Check file size limit
    image.seek(0, io.SEEK_END)  # Move to end of file to get size
    file_size = image.tell()  # Get file size in bytes
    image.seek(0)  # Reset file pointer

    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 2MB limit"}), 400

    # Check existing image count for API key
    existing_record = api_keys_collection.find_one({"api_key": api_key})
    if existing_record:
        return jsonify({"error": "API key can only store one profile picture"}), 400

    image_id = fs.put(image, filename=image.filename)
    api_keys_collection.insert_one({"api_key": api_key, "image_id": image_id})

    return jsonify({"message": "Image uploaded successfully", "image_id": str(image_id)})

# Fetch Image by API Key
@app.route('/fetch', methods=['GET'])
def fetch_image():
    api_key = request.headers.get("API-Key")
    if not api_key:
        return jsonify({"error": "API key required"}), 400

    record = api_keys_collection.find_one({"api_key": api_key})
    if not record:
        return jsonify({"error": "No image found for this API key"}), 404

    image_id = record["image_id"]
    image_data = fs.get(image_id)

    return send_file(io.BytesIO(image_data.read()), mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(debug=True)