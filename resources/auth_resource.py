from flask_restful import Resource
from flask import request

from models.user import User
from utils.jwt_helper import generate_token


class LoginResource(Resource):

    def post(self):

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(
            organization_id=data["organization_id"],
            username=data["username"]
        ).first()

        if not user or user.password != password:
            return {"message": "Invalid credentials"}, 401

        token = generate_token(user.id)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "organization_id": user.organization_id,
                "role": user.role
            }
        }