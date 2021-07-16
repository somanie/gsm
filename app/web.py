# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import random
# from . import gsm

# app = Flask(__name__)
# db = SQLAlchemy(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     name = db.Column(db.String(50))
#     IMSI = db.Column(db.String(20))
#     call_duration = db.Column(db.Integer)

#     def __init__(self, **kwargs):
#         self.IMSI = str(random.randint(100_000_000_000_000, 999_999_999_999_999))
#         kwargs["IMSI"] = self.IMSI

#         super().__init__(**kwargs)

#     def __repr__(self) -> str:
#         return self.name

# db.create_all()

# env = gsm.env
# vlr = gsm.vlr
# auc = gsm.auc
# msc = gsm.msc
# bss = gsm.bss
# Subscriber = gsm.Subscriber

# @app.route("/")
# @app.route("/<string:duration>")
# def index(duration="predetermined"):
#     if duration.lower() == 'random':
#         randomness = True
#     else:
#         randomness = False

#     users = User.query.all()
#     for user in users:
#         sub = Subscriber(
#                         env, 
#                         user.name, 
#                         bss, 
#                         random.randint(9, 150) if randomness else user.call_duration, 
#                         user.IMSI)
#         print(f"{sub.name}'s call duration is {sub.call_duration}")
#     env.run()
#     return "Hello World"

# if __name__ == "__main__":
#     app.run(debug=True)