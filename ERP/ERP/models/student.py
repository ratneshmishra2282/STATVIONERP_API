
from extensions import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.Integer, index=True)
    mongo_id = db.Column(db.String(50))

    name = db.Column(db.String(150))
    scholar_no = db.Column(db.String(50))
    roll_no = db.Column(db.String(50))
    class_name = db.Column(db.String(100))
    course = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    total_fee = db.Column(db.Float, default=0)
    paid_fee = db.Column(db.Float, default=0)
    due_fee = db.Column(db.Float, default=0)

    status = db.Column(db.String(20), default="active")
