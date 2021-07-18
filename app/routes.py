from flask import Blueprint, render_template, redirect, url_for, request
from app.models import db, User
from app import gsm
import random
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegistrationForm, LoginForm

bp = Blueprint("main", __name__)

env = gsm.env
vlr = gsm.vlr
auc = gsm.auc
msc = gsm.msc
bss = gsm.bss
Subscriber = gsm.Subscriber

@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        # new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        if form.sign_in.data:
            login_user(new_user)
            return redirect(url_for('main.index'))
        return redirect(url_for('main.login'))
    return render_template("register.html", form=form, title="Sign Up")

@bp.route("/login", methods= ['GET', "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.index"))

    return render_template("login.html", form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@bp.route("/")
def index():
    return render_template("dashboard.html")
    # return "Hello World"

@bp.route("/simulation")
@bp.route("/simulation/<string:duration>")
def simulation(duration="predetermined"):
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
    return render_template("simulation.html")