from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URI')
    login_manager.init_app(app)
    db.init_app(app)
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

    from .routes import bp
    app.register_blueprint(bp)

    return app
