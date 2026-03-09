
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.fee import Fee
from models.student import Student
from extensions import db

fee_bp = Blueprint("fees", __name__)

from services.whatsapp_service import send_fee_submission_message


@fee_bp.route("/fees", methods=["POST"])
@jwt_required()
def submit_fee():

    data = request.json

    student = Student.query.get(data["student_id"])

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # 1️⃣ Save fee transaction
    fee = Fee(
        student_id=student.id,
        organization_id=student.organization_id,
        amount=data["amount"],
        payment_mode=data.get("payment_mode", "cash")
    )

    db.session.add(fee)

    # 2️⃣ Update aggregated fee
    student.paid_fee += data["amount"]
    student.due_fee = student.total_fee - student.paid_fee

    db.session.commit()

    # 3️⃣ Send WhatsApp message
    try:
        if student.phone:
            send_fee_submission_message(
                phone=student.phone,
                student_name=student.name,
                amount=data["amount"],
                due_fee=student.due_fee
            )
    except Exception as e:
        print("WhatsApp error:", e)

    return jsonify({
        "message": "Fee submitted successfully",
        "due_fee": student.due_fee
    })