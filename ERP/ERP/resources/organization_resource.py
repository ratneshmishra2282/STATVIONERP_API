
from flask import Blueprint, request, jsonify
from models.organization import Organization
from extensions import db

org_bp = Blueprint("org", __name__)

@org_bp.route("/organizations", methods=["POST"])
def create_org():
    data = request.json

    org = Organization(
        name=data["name"],
        type=data["type"],
        subdomain=data["subdomain"],
        plan="basic"
    )

    db.session.add(org)
    db.session.commit()

    return jsonify({"message":"Organization created"})
