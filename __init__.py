from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
# from numpy import random as rand

import os
# from apscheduler.schedulers.background import BackgroundScheduler
# import datetime
# import uuid

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom(24)

    # scheduler = BackgroundScheduler()
    # scheduler.start()

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    mail = Mail(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint for auth routes in our app
    from Website.user.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .bracket import bracket as bracket_blueprint
    app.register_blueprint(bracket_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # steganography

    from Website.main.mandelbrot_web import mandelbrot_web as mandelbrot_blueprint
    app.register_blueprint(mandelbrot_blueprint)

    from Website.main.steganography_web import steganography_web as steganography_blueprint
    app.register_blueprint(steganography_blueprint)

    return app

my_app = create_app()