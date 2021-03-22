from flask import Blueprint
from flask_login import login_required
# from . import db

bracket = Blueprint('bracket', __name__)

@bracket.route('/projects/bracket/standings')
@login_required
def standings():
    return 'standings Success'


@bracket.route('/projects/bracket/my_bracket')
@login_required
def my_bracket():
    return 'my_bracket Success'

# @bracket.route('/')
# def profile():
#     return 'Profile'