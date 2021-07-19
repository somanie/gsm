from operator import imod
from flask import Blueprint, render_template, redirect, url_for, request
from app.models import db, User, Subscriber
from app import gsm
import random
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegistrationForm, LoginForm
from app.utils import generate_simulation

bp = Blueprint("main", __name__)



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
    return redirect(url_for('main.simulation'))

# @bp.route("/simulation")
@bp.route("/simulation")
def simulation():
    if range := request.args.get('range'):
        if request.args.get('random'):
            sim = generate_simulation(random=True)
        else:
            sim = generate_simulation(_range=range)
        
        return render_template("simulation.html", values=sim)
    
    else:
        return render_template("simulation.html", values=[0*24])