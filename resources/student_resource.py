from flask_restful import Resource
from flask import request
from sqlalchemy.sql.functions import current_user

from models.student import Student
from extensions import db, mongo
from bson import ObjectId
from decorator.auth_decorator import login_required


class StudentListResource(Resource):

    @login_required
    def get(self):

        current_user = request.user
        org_id = current_user.organization_id

        last_id = request.args.get("last_id", type=int)
        limit = request.args.get("limit", 20, type=int)

        query = Student.query.filter_by(
            organization_id=org_id
        ).order_by(Student.id.asc())

        if last_id:
            query = query.filter(Student.id > last_id)

        students = query.limit(limit).all()

        data = []

        for s in students:
            data.append({
                "id": s.id,
                "name": s.name,
                "class": s.class_name,
                "phone": s.phone,
                "total_fee": s.total_fee,
                "paid_fee": s.paid_fee,
                "due_fee": s.due_fee
            })

        next_cursor = students[-1].id if len(students) == limit else None

        return {
            "data": data,
            "next_cursor": next_cursor
        }

    @login_required
    def post(self):

        data = request.json
        user = get_jwt_identity()
        org_id = user["organization_id"]

        student = Student(
            organization_id=org_id,
            name=data["name"],
            class_name=data.get("class_name"),
            phone=data.get("phone"),
            total_fee=data.get("total_fee", 0),
            due_fee=data.get("total_fee", 0)
        )

        db.session.add(student)
        db.session.commit()

        mongo_data = {
            "sql_student_id": student.id,
            "extra_data": data.get("extra_data", {})
        }

        result = mongo.db.students_profile.insert_one(mongo_data)

        student.mongo_id = str(result.inserted_id)
        db.session.commit()

        return {"student_id": student.id}, 201


class StudentDetailResource(Resource):

    @login_required
    def get(self, student_id):

        current_user = request.user
        org_id = current_user.organization_id

        student = Student.query.filter_by(
            id=student_id,
            organization_id=org_id
        ).first()

        if not student:
            return {"error": "Student not found"}, 404

        extra_data = {}

        if student.mongo_id:
            profile = mongo.db.students_profile.find_one({
                "_id": ObjectId(student.mongo_id)
            })

            if profile:
                profile["_id"] = str(profile["_id"])
                extra_data = profile

        return {
            "student": {
                "id": student.id,
                "name": student.name,
                "class": student.class_name,
                "phone": student.phone
            },
            "fee_summary": {
                "total_fee": student.total_fee,
                "paid_fee": student.paid_fee,
                "due_fee": student.due_fee
            },
            "extra_data": extra_data
        }