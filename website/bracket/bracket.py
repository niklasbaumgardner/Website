from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_user, current_user, logout_user, login_required
# from . import db

bracket = Blueprint('bracket', __name__)

@bracket.route('/projects/bracket/standings')
@login_required
def standings():
    return render_template("standings.html")


@bracket.route('/projects/bracket/my_bracket')
@login_required
def my_bracket():
    return render_template("my_bracket.html")

# @bracket.route('/')
# def profile():
#     return 'Profile'