from flask_restful import Resource
from flask import request

from extensions import db
from decorator.auth_decorator import login_required
from models.user import User


class CreateUserResource(Resource):

    @login_required()
    def post(self):

        current_user = request.user

        if current_user.role != "admin":
            return {"message": "Only admin can create users"}, 403

        data = request.get_json()
        existing = User.query.filter_by(
            organization_id=current_user.organization_id,
            username=data["username"]
        ).first()

        if existing:
            return {"message": "Username already exists in your organization"}, 400

        user = User(
            organization_id=current_user.organization_id,
            username=data["username"],
            password=data["password"],
            role=data.get("role", "staff")
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}