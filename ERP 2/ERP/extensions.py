from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api

db = SQLAlchemy()
jwt = JWTManager()
mongo = PyMongo()
api = Api()