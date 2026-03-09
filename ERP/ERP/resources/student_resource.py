
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.student import Student
from extensions import db, mongo
from bson import ObjectId
student_bp = Blueprint("students", __name__)

@student_bp.route("/students", methods=["POST"])
@jwt_required()
def create_student():
    data = request.json
    user = get_jwt_identity()
    org_id = user["organization_id"]

    student = Student(
        organization_id=org_id,
        name=data["name"],
        class_name=data.get("class_name"),
        phone=data.get("phone"),
        total_fee=data.get("total_fee",0),
        due_fee=data.get("total_fee",0)
    )

    db.session.add(student)
    db.session.commit()

    mongo_data = {
        "sql_student_id": student.id,
        "extra_data": data.get("extra_data",{})
    }

    result = mongo.db.students_profile.insert_one(mongo_data)

    student.mongo_id = str(result.inserted_id)
    db.session.commit()

    return jsonify({"student_id":student.id})

@student_bp.route("/students/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):

    current_user = get_jwt_identity()
    org_id = current_user["organization_id"]

    # 1️⃣ Get student from SQL
    student = Student.query.filter_by(
        id=student_id,
        organization_id=org_id
    ).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # 2️⃣ Get extra profile from Mongo
    extra_data = {}

    if student.mongo_id:
        mongo_profile = mongo.db.students_profile.find_one({
            "_id": ObjectId(student.mongo_id)
        })

        if mongo_profile:
            mongo_profile["_id"] = str(mongo_profile["_id"])
            extra_data = mongo_profile

    # 3️⃣ Return merged response
    return jsonify({

        "student": {
            "id": student.id,
            "name": student.name,
            "scholar_no": student.scholar_no,
            "roll_no": student.roll_no,
            "class": student.class_name,
            "course": student.course,
            "phone": student.phone,
            "status": student.status
        },

        "fee_summary": {
            "total_fee": student.total_fee,
            "paid_fee": student.paid_fee,
            "due_fee": student.due_fee
        },

        "extra_data": extra_data

    }), 200

