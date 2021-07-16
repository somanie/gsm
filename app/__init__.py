from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
# import random
# from . import gsm

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URI')
    db.init_app(app)
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

    from .routes import bp
    app.register_blueprint(bp)

    return app
