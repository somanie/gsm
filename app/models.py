from app import db, login_manager
import random
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)
        # super().__init__(password=password, username=kwargs["username"])

    def __repr__(self) -> str:
        return self.username

    def set_password(self, password):
        hash_ = generate_password_hash(password, method="sha256")
        self.password = hash_
        # return hash_

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    IMSI = db.Column(db.String(20))
    call_duration = db.Column(db.Integer)
    # calls_sent = db.relationship("Call", backref="caller")
    # calls_received = db.relationship("Call", backref="receiver")

    def __init__(self, **kwargs):
        self.IMSI = str(random.randint(100_000_000_000_000, 999_999_999_999_999))
        kwargs["IMSI"] = self.IMSI

        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return self.name

class Simulation(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    # calls = db.relationship("Call", backref="simulation")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    caller_id = db.Column(db.Integer, db.ForeignKey("subscriber.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("subscriber.id"), nullable=False)
    simualation_id = db.Column(db.Integer, db.ForeignKey("simulation.id"), nullable=False)

    caller = db.relationship("Subscriber", backref="calls_sent", foreign_keys=[caller_id])
    receiver = db.relationship("Subscriber", backref="calls_receiver", foreign_keys=[receiver_id])
    simulation = db.relationship("Simulation", backref="calls")
