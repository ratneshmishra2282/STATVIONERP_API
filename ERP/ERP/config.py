
class Config:
    SECRET_KEY = "supersecret"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/erp"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret"
    MONGO_URI = "mongodb://localhost:27017/erp"
