from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from website import bcrypt
from website.extensions import db, login_manager
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
        next_page = request.args.get('next')
        return redirect(next_page or url_for('bracket.view_bracket'))
    
    elif user:
        flash('Password was incorrect. Try again', 'w3-pale-red')
        return render_template("login.html", email=email)

    flash('User not found. Please create an acount', 'w3-pale-red')

    return render_template("login.html", email=email)

@auth.route('/bracket/signup')
def signup():
    return render_template("signup.html")

@auth.route('/bracket/signup', methods=["POST"])
def signup_post():
    try:

        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists. Please log in', 'w3-pale-red')
            return render_template("login.html", email=email)

        if password1 != password2:
            flash('Passwords don\'t match. Try again', 'w3-pale-red')
            return render_template("signup.html", email=email)
        hash_ = bcrypt.generate_password_hash(password1).decode('utf-8')

        new_user = User(email=email, password=hash_)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up succesful', 'w3-pale-green')
        return render_template("login.html", email=email)
    
    except:
        flash('Sign up failed', 'w3-pale-red')
    
    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))