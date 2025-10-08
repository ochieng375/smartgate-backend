from flask import Blueprint, request, jsonify
from config import students, logs
from utils.barcode_reader import decode_barcode
import datetime

gate = Blueprint("gate", __name__)

@gate.route("/scan-barcode", methods=["POST"])
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
        "status": "granted"
    })

    return jsonify(student)

@gate.route("/manual-access", methods=["POST"])
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
