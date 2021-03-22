# from flask import Flask, escape, request, render_template, url_for, redirect, session, flash
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_mail import Mail, Message
from website import mail
# from numpy import random as rand
# import mandelbrot as mandel
# import steganography as steg
# import os
# from apscheduler.schedulers.background import BackgroundScheduler
# import datetime
# import uuid


# app = Flask(__name__)

home = Blueprint('home', __name__)
# mail = Mail(home)

@home.route('/', methods=["GET"])
def index():
    return render_template('index.html')



@home.route("/projects/", methods=["GET"])
def projects():
    return render_template("projects.html")

@home.route("/contact/", methods=["GET"])
def contact():
    return render_template("contact.html")

@home.route("/send/", methods=["POST"])
def send():

    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        emailMessage = Message(subject=subject, sender='noreply', recipients=[email, "baumga91@msu.edu"], body=message)

        mail.send(emailMessage)

        flash('Email successfully sent!', 'w3-pale-green')
    except:
        flash('Email failed to send', 'w3-pale-red')

    return redirect(url_for('home.contact'))




# set FLASK_APP=hello.py
# $env:FLASK_APP = "hello.py"
# WSL
# export FLASK_APP=home.py
# flask run


# $site->dbConfigure('mysql:host=mysql-user.cse.msu.edu;dbname=baumga91',
#         'baumga91',       // Database user
#         'password',     // Database password
#         '');            // Table prefix


# if __name__ == '__main__':
#     app.run(debug=True)
    # app.run()

