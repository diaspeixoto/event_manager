from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

db = SQLAlchemy()
mongo_db = PyMongo()

def init_db(app):
    db.init_app(app)
    mongo_db.init_app(app)
    
