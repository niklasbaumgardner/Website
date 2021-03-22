from flask import Blueprint
# from . import db

bracket = Blueprint('bracket', __name__)

@bracket.route('/projects/bracket/')
def index():
    return 'Index'

# @bracket.route('/')
# def profile():
#     return 'Profile'