from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_restful import Api

db = SQLAlchemy()
mongo = PyMongo()
# api = Api()