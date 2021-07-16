from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
# import random
# from . import gsm

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL')

    return app
