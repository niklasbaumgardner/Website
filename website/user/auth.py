from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user
from website import db, bcrypt, login_manager
from website.models import User

auth = Blueprint('auth', __name__)

@auth.route('/bracket/login')
def login():
    return render_template("login.html")

@auth.route('/bracket/login', methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # add remember me button
        login_user(user)
        return redirect(url_for('bracket.standings'))

    return render_template("login.html")

@auth.route('/bracket/signup')
def signup():
    return render_template("signup.html")

@auth.route('/bracket/signup', methods=["POST"])
def signup_post():
    try:

        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        hash_ = bcrypt.generate_password_hash(password1).decode('utf-8')

        # check if email in db
        # User.query.first()
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please log in', 'w3-pale-red')
            return render_template("login.html")

        new_user = User(email=email, password=hash_)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up succesful', 'w3-pale-green')
        return render_template("login.html")
    
    except:
        flash('Sign up failed', 'w3-pale-red')
    
    return render_template("signup.html")

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))