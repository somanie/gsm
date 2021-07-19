from faker import Faker
from app.models import db, Subscriber

fake = Faker()

def generate_subscribers(amount):
    for i in range(amount):
        sub = Subscriber()
        sub.name = fake.name()
        sub.call_duration = fake.pyint(max_value=150)
        db.session.add(sub)

    db.session.commit()

def generate_simulation(random=False, _range=80):
    if not random:
        _range = fake.pyint(min_value=30, max_value=100)

    values = []
    for value in range(24):
        values.append(fake.pyint(max_value=_range))

    return values

        
