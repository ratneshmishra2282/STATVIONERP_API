
from extensions import db

class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    type = db.Column(db.String(50))
    subdomain = db.Column(db.String(100), unique=True)
    plan = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
