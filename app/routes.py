from flask import current_app as app
from app.models import User
from app import gsm
import random

env = gsm.env
vlr = gsm.vlr
auc = gsm.auc
msc = gsm.msc
bss = gsm.bss
Subscriber = gsm.Subscriber

@app.route("/")
@app.route("/<string:duration>")
def index(duration="predetermined"):
    if duration.lower() == 'random':
        randomness = True
    else:
        randomness = False

    users = User.query.all()
    for user in users:
        sub = Subscriber(
                        env, 
                        user.name, 
                        bss, 
                        random.randint(9, 150) if randomness else user.call_duration, 
                        user.IMSI)
        print(f"{sub.name}'s call duration is {sub.call_duration}")
    env.run()
    return "Hello World"