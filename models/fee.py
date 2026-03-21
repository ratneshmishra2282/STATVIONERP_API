
from extensions import db
from datetime import datetime

class Fee(db.Model):
    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.BigInteger, index=True)
    organization_id = db.Column(db.Integer, index=True)
    amount = db.Column(db.Float)
    payment_mode = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
