from flask import Blueprint, redirect, url_for, render_template, request
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

@bracket.route('/projects/bracket/submit_bracket', methods=['POST'])
@login_required
def submit_bracket():
    game1 = request.form.get('game1')
    game2 = request.form.get('game2')
    game3 = request.form.get('game3')
    game4 = request.form.get('game4')
    game5 = request.form.get('game5')
    game6 = request.form.get('game6')
    game7 = request.form.get('game7')
    game8 = request.form.get('game8')
    game9 = request.form.get('game9')
    game10 = request.form.get('game10')
    game11 = request.form.get('game11')
    game12 = request.form.get('game12')
    game13 = request.form.get('game13')
    game14 = request.form.get('game14')
    game15 = request.form.get('game15')
    print(game1, game2, game3, game4, game5, game6, game7, game8, game9, game10, game11, game12, game13, game14, game15)
    return render_template("my_bracket.html") 