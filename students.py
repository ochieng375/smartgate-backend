def create_student(data, db):
    student = {
        "name": data["name"],
        "student_id": data["student_id"],
        "email": data["email"],
        "laptop_serial": data.get("laptop_serial"),
        "barcode": data.get("barcode")
    }
    db.insert_one(student)
    return student
