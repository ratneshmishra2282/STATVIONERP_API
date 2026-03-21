from flask_restful import Resource
from flask import request
from extensions import db
from models.fee import Fee
from models.student import Student
from services.whatsapp_service import send_fee_submission_message
from decorator.auth_decorator import login_required


class FeeResource(Resource):

    @login_required
    def post(self):

        data = request.json

        student = Student.query.get(data["student_id"])

        fee = Fee(
            student_id=student.id,
            organization_id=student.organization_id,
            amount=data["amount"],
            payment_mode=data.get("payment_mode", "cash")
        )

        db.session.add(fee)

        student.paid_fee += data["amount"]
        student.due_fee = student.total_fee - student.paid_fee

        db.session.commit()

        # send whatsapp
        if student.phone:
            send_fee_submission_message(
                student.phone,
                student.name,
                data["amount"],
                student.due_fee
            )

        return {"message": "Fee submitted"}