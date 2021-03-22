from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from numpy import random as rand

import os

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ['SECRET_KEY']

    app.config['TESTING'] = False

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'w3-pale-red'

    # blueprint for auth routes in our app
    from website.user.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from website.bracket.bracket import bracket as bracket_blueprint
    app.register_blueprint(bracket_blueprint)

    from website.main.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # steganography

    from website.mandelbrot.mandelbrot_web import mandelbrot_web as mandelbrot_blueprint
    app.register_blueprint(mandelbrot_blueprint)

    from website.steganography.steganography_web import steganography_web as steganography_blueprint
    app.register_blueprint(steganography_blueprint)

    return app

# my_app = create_app()