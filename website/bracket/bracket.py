from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from website.extensions import db
from website.models import Bracket
# from . import db

bracket = Blueprint('bracket', __name__)

@bracket.route('/projects/bracket/standings')
def standings():
    brackets = Bracket.query.all()
    return render_template("standings.html", brackets=brackets, enumerate=enumerate)

@bracket.route('/projects/bracket/edit_bracket')
@login_required
def edit_bracket():
    bracket = Bracket.query.filter_by(user_id=current_user.get_id()).first()
    if bracket:
        return render_template("edit_bracket.html", bracket=bracket)

    return render_template("edit_bracket.html", bracket=bracket)

@bracket.route('/projects/bracket/view_bracket', defaults={'id': None})
@bracket.route('/projects/bracket/view_bracket/<int:id>')
def view_bracket(id):
    if id:
        bracket = Bracket.query.filter_by(id=id).first()
        # print(bracket.user_id, current_user.get_id())
        # print(type(bracket.user_id), type(current_user.get_id()))
        if current_user.is_authenticated:
            return render_template("view_bracket.html", bracket=bracket, user_id=int(current_user.get_id()))
        return render_template("view_bracket.html", bracket=bracket)
    else:
        if current_user.is_authenticated:
            bracket = Bracket.query.filter_by(user_id=current_user.get_id()).first()
            # print(bracket.user_id, current_user.get_id())
            # print(type(bracket.user_id), type(current_user.get_id()))
            return render_template("view_bracket.html", bracket=bracket, user_id=int(current_user.get_id()))
            

    return render_template("standings.html")

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
    name = request.form.get('name')
    w_goals = request.form.get('w_goals')
    l_goals = request.form.get('l_goals')
    print(game1, game2, game3, game4, game5, game6, game7, game8, game9, game10, game11, game12, game13, game14, game15)

    new_bracket = Bracket(user_id=current_user.get_id(), name=name, year=datetime.today().year, game1=game1, game2=game2,
    game3=game3, game4=game4, game5=game5, game6=game6, game7=game7, game8=game8, game9=game9, game10=game10,
    game11=game11, game12=game12, game13=game13, game14=game14, game15=game15, w_goals=w_goals, l_goals=l_goals,
    max_points=1000, points=0)

    existing_bracket = Bracket.query.filter_by(user_id=current_user.get_id()).first()

    if existing_bracket:
        existing_bracket.game1 = new_bracket.game1
        existing_bracket.game2 = new_bracket.game2
        existing_bracket.game3 = new_bracket.game3
        existing_bracket.game4 = new_bracket.game4
        existing_bracket.game5 = new_bracket.game5
        existing_bracket.game6 = new_bracket.game6
        existing_bracket.game7 = new_bracket.game7
        existing_bracket.game8 = new_bracket.game8
        existing_bracket.game9 = new_bracket.game9
        existing_bracket.game10 = new_bracket.game10
        existing_bracket.game11 = new_bracket.game11
        existing_bracket.game12 = new_bracket.game12
        existing_bracket.game13 = new_bracket.game13
        existing_bracket.game14 = new_bracket.game14
        existing_bracket.game15 = new_bracket.game15

        existing_bracket.w_goals = new_bracket.w_goals
        existing_bracket.l_goals = new_bracket.l_goals

        existing_bracket.name = new_bracket.name

        existing_bracket.max_points = new_bracket.max_points
        existing_bracket.points = new_bracket.points

        db.session.commit()
    
    else:
        db.session.add(new_bracket)
        db.session.commit()

    # return render_template("view_bracket.html")
    return redirect(url_for('bracket.view_bracket'))