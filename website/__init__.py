from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from website.config import Config
from website.commands import create_tables
# from numpy import random as rand
from website.extensions import db, login_manager
import psycopg2
import os

mail = Mail()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

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
