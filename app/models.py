from app import db
import random


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    IMSI = db.Column(db.String(20))
    call_duration = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.IMSI = str(random.randint(100_000_000_000_000, 999_999_999_999_999))
        kwargs["IMSI"] = self.IMSI

        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return self.name