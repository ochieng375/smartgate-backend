from flask import Blueprint, jsonify
from config import logs, students

admin = Blueprint("admin", __name__)

@admin.route("/students", methods=["GET"])
def get_students():
    return jsonify(list(students.find({}, {"_id": 0})))

@admin.route("/access-logs", methods=["GET"])
def get_logs():
    return jsonify(list(logs.find({}, {"_id": 0})))
