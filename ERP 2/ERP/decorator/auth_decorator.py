from functools import wraps
from flask import request, jsonify

from utils.jwt_helper import decode_token
from models.user import User


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"message": "Token missing"}, 401

        token = auth_header.split(" ")[1]

        user_id = decode_token(token)

        if not user_id:
            return {"message": "Invalid or expired token"}, 401

        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        request.user = user

        return func(*args, **kwargs)

    return wrapper