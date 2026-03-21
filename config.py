import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI","mysql+pymysql://admin:EZgvlO2wWlvzCfDnM0wS@erpprod.c98mq6ouy2rp.ap-south-1.rds.amazonaws.com/erp")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/erp")
