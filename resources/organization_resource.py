from flask_restful import Resource
from flask import request

from extensions import db
from models.organization import Organization
from models.user import User


class OrganizationRegisterResource(Resource):

    def post(self):

        data = request.get_json()

        org = Organization(
            name=data["name"],
            phone=data["phone"],
            email=data.get("email"),
            address=data.get("address")
        )

        db.session.add(org)
        db.session.flush()   # get org id

        admin = User(
            organization_id=org.id,
            username=data["admin_username"],
            password=data["admin_password"],
            role="admin"
        )

        db.session.add(admin)

        db.session.commit()

        return {
            "message": "Organization registered successfully",
            "organization_id": org.id
        }, 201