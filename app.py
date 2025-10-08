from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient("your MongoDB Atlas URI here")
db = client.smartgate
students = db.students
logs = db.access_logs

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

# Get all students
@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(list(students.find({}, {"_id": 0})))

# Get access logs
@app.route("/api/access-logs", methods=["GET"])
def get_logs():
    return jsonify(list(logs.find({}, {"_id": 0})))

# Submit incident report (optional)
@app.route("/api/incidents", methods=["POST"])
def report_incident():
    data = request.json
    db.incidents.insert_one({
        "student_id": data.get("student_id"),
        "description": data.get("description"),
        "timestamp": datetime.datetime.now()
    })
    return jsonify({"message": "Incident submitted"}), 200

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
