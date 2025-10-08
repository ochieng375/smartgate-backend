from flask import Flask, request, jsonify
from pymongo import MongoClient
from pyzbar.pyzbar import decode
from PIL import Image
import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient("your MongoDB Atlas URI here")
db = client.smartgate
students = db.students
logs = db.access_logs

# Barcode reader
def decode_barcode(image_path):
    image = Image.open(image_path)
    result = decode(image)
    return result[0].data.decode("utf-8") if result else None

# Barcode scan route
@app.route("/api/scan-barcode", methods=["POST"])
def scan_barcode():
    image = request.files["image"]
    path = f"uploads/{image.filename}"
    image.save(path)

    barcode = decode_barcode(path)
    if not barcode:
        return jsonify({"error": "Barcode not readable"}), 400

    student = students.find_one({"barcode": barcode})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    logs.insert_one({
        "student_id": student["student_id"],
        "timestamp": datetime.datetime.now(),
        "method": "barcode",
        "status": "granted",
        "reason": "Barcode match"
    })

    return jsonify(student)

# Manual access route
@app.route("/api/manual-access", methods=["POST"])
def manual_access():
    data = request.json
    student = students.find_one({"student_id": data["student_id"]})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    logs.insert_one({
        "student_id": student["student_id"],
        "timestamp": datetime.datetime.now(),
        "method": "manual",
        "status": "granted",
        "reason": "Fallback"
    })

    return jsonify(student)

# Admin routes
@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(list(students.find({}, {"_id": 0})))

@app.route("/api/access-logs", methods=["GET"])
def get_logs():
    return jsonify(list(logs.find({}, {"_id": 0})))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)


