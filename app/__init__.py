from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import random
# from . import gsm

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    return app
