from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from pytz import timezone
from website.extensions import db, TEAMS
from website.models import Bracket
from website import bcrypt
import os
# from . import db

bracket = Blueprint('bracket', __name__)
TIMEZONE = timezone('EST')
FIRST_GAME = datetime(year=2021, month=3, day=26, hour=13, tzinfo=TIMEZONE)

@bracket.route('/bracket/correct_bracket')
@login_required
def orrect_bracket():
    CORRECT_BRACKET = Bracket.query.filter_by(name='CORRECT_BRACKET', id=0).first()
    return render_template('correct_bracket.html', bracket=CORRECT_BRACKET)

@bracket.route('/bracket/update_correct_bracket', methods=["POST"])
@login_required
def update_correct_bracket():
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

    password = request.form.get('password')
    correct_pass = os.environ.get('CORRECT_PASSWORD')

    if bcrypt.check_password_hash(correct_pass, password):
        new_bracket = Bracket(game1=game1, game2=game2,
            game3=game3, game4=game4, game5=game5, game6=game6, game7=game7, game8=game8, game9=game9, game10=game10,
            game11=game11, game12=game12, game13=game13, game14=game14, game15=game15)
        
        CORRECT_BRACKET = Bracket.query.filter_by(name='CORRECT_BRACKET', id=0).first()

        CORRECT_BRACKET.game1 = new_bracket.game1
        CORRECT_BRACKET.game2 = new_bracket.game2
        CORRECT_BRACKET.game3 = new_bracket.game3
        CORRECT_BRACKET.game4 = new_bracket.game4
        CORRECT_BRACKET.game5 = new_bracket.game5
        CORRECT_BRACKET.game6 = new_bracket.game6
        CORRECT_BRACKET.game7 = new_bracket.game7
        CORRECT_BRACKET.game8 = new_bracket.game8
        CORRECT_BRACKET.game9 = new_bracket.game9
        CORRECT_BRACKET.game10 = new_bracket.game10
        CORRECT_BRACKET.game11 = new_bracket.game11
        CORRECT_BRACKET.game12 = new_bracket.game12
        CORRECT_BRACKET.game13 = new_bracket.game13
        CORRECT_BRACKET.game14 = new_bracket.game14
        CORRECT_BRACKET.game15 = new_bracket.game15

        db.session.commit()

        return redirect(url_for('bracket.update_points'))

    return redirect(url_for('bracket.standings'))

@bracket.route('/bracket/standings')
def standings():
    clickable = False
    brackets = Bracket.query.filter(Bracket.name != 'CORRECT_BRACKET').filter(Bracket.id !=0).all()
    brackets.sort(key=lambda b: b.max_points, reverse=True)
    brackets.sort(key=lambda b: b.points, reverse=True)
    rank = 1
    standings = []
    for i, bracket in enumerate(brackets):
        if i == 0:
            standings.append((rank, bracket))
        elif bracket.points == brackets[i - 1].points:
            standings.append((rank, bracket))
        else:
            rank = i + 1
            standings.append((i, bracket))

    if datetime.now(TIMEZONE) > FIRST_GAME:
        clickable = True
    
    return render_template("standings.html", brackets=standings, enumerate=enumerate, clickable=clickable)


@bracket.route('/bracket/edit_bracket')
@login_required
def edit_bracket():
    if datetime.now(TIMEZONE) > FIRST_GAME:
        return redirect(url_for('bracket.view_bracket'))

    bracket = Bracket.query.filter_by(user_id=current_user.get_id()).first()

    return render_template("edit_bracket.html", bracket=bracket)


@bracket.route('/bracket/view_bracket', defaults={'id': None})
@bracket.route('/bracket/view_bracket/<int:id>')
def view_bracket(id):
    # keep as if id:

    if datetime.now(TIMEZONE) > FIRST_GAME:
        CORRECT_BRACKET = Bracket.query.filter_by(name='CORRECT_BRACKET', id=0).first()
        if id:
            bracket = Bracket.query.filter_by(id=id).first()
            return render_template("view_bracket.html", bracket=bracket, correct=CORRECT_BRACKET)

        elif current_user.is_authenticated:
            curr_user_id = int(current_user.get_id())
            bracket = Bracket.query.filter_by(user_id=curr_user_id).first()
            return render_template("view_bracket.html", bracket=bracket, correct=CORRECT_BRACKET)
    else:
        if current_user.is_authenticated:
            curr_user_id = int(current_user.get_id())
            if not id or (id and id == curr_user_id):
                bracket = Bracket.query.filter_by(user_id=curr_user_id).first()
                return render_template("view_bracket.html", bracket=bracket, user_id=curr_user_id)
            else:
                return redirect(url_for('bracket.standings'))

    flash('Login to view your bracket', 'w3-pale-red')
    return redirect(url_for('auth.login'))


@bracket.route('/bracket/submit_bracket', methods=['POST'])
@login_required
def submit_bracket():
    if datetime.now(TIMEZONE) > FIRST_GAME:
        return redirect(url_for('bracket.view_bracket'))

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
    # print(game1, game2, game3, game4, game5, game6, game7, game8, game9, game10, game11, game12, game13, game14, game15)

    new_bracket = Bracket(user_id=current_user.get_id(), name=name, year=datetime.today().year, game1=game1, game2=game2,
    game3=game3, game4=game4, game5=game5, game6=game6, game7=game7, game8=game8, game9=game9, game10=game10,
    game11=game11, game12=game12, game13=game13, game14=game14, game15=game15, w_goals=w_goals, l_goals=l_goals,
    max_points=320, points=0)

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

        # existing_bracket.max_points = new_bracket.max_points
        # existing_bracket.points = new_bracket.points

        db.session.commit()
    
    else:
        db.session.add(new_bracket)
        db.session.commit()

    # return render_template("view_bracket.html")
    return redirect(url_for('bracket.view_bracket'))


@bracket.route('/bracket/update_points')
@login_required
def update_points():
    CORRECT_BRACKET = Bracket.query.filter_by(name='CORRECT_BRACKET', id=0).first()
    brackets = Bracket.query.filter(Bracket.name != 'CORRECT_BRACKET').filter(Bracket.id !=0).all()
    
    for bracket in brackets:
        update_bracket_points(bracket, CORRECT_BRACKET)
    db.session.commit()
    return redirect(url_for('bracket.standings'))


def update_bracket_points(bracket, CORRECT_BRACKET):

    points = 0

    # ROUND 1
    if bracket.game1 == CORRECT_BRACKET.game1:
        points += 10
    if bracket.game2 == CORRECT_BRACKET.game2:
        points += 10
    if bracket.game3 == CORRECT_BRACKET.game3:
        points += 10
    if bracket.game4 == CORRECT_BRACKET.game4:
        points += 10
    if bracket.game5 == CORRECT_BRACKET.game5:
        points += 10
    if bracket.game6 == CORRECT_BRACKET.game6:
        points += 10
    if bracket.game7 == CORRECT_BRACKET.game7:
        points += 10
    if bracket.game8 == CORRECT_BRACKET.game8:
        points += 10

    # ROUND 2
    if bracket.game9 == CORRECT_BRACKET.game9:
        points += 20
    if bracket.game10 == CORRECT_BRACKET.game10:
        points += 20
    if bracket.game11 == CORRECT_BRACKET.game11:
        points += 20
    if bracket.game12 == CORRECT_BRACKET.game12:
        points += 20

    # ROUND 3
    if bracket.game13 == CORRECT_BRACKET.game13:
        points += 40
    if bracket.game14 == CORRECT_BRACKET.game14:
        points += 40

    # WINNER
    if bracket.game15 == CORRECT_BRACKET.game15:
        points += 80

    bracket.points = points
    bracket.max_points = update_max(bracket, CORRECT_BRACKET)


def update_max(bracket, CORRECT_BRACKET):
    max_points = 0

    # ROUND 1
    game1 = False
    game2 = False
    game3 = False
    game4 = False
    game5 = False
    game6 = False
    game7 = False
    game8 = False
    if CORRECT_BRACKET.game1 not in TEAMS or bracket.game1 == CORRECT_BRACKET.game1:
        max_points += 10
        game1 = True
    if CORRECT_BRACKET.game2 not in TEAMS or bracket.game2 == CORRECT_BRACKET.game2:
        max_points += 10
        game2 = True
    if CORRECT_BRACKET.game3 not in TEAMS or bracket.game3 == CORRECT_BRACKET.game3:
        max_points += 10
        game3 = True
    if CORRECT_BRACKET.game4 not in TEAMS or bracket.game4 == CORRECT_BRACKET.game4:
        max_points += 10
        game4 = True
    if CORRECT_BRACKET.game5 not in TEAMS or bracket.game5 == CORRECT_BRACKET.game5:
        max_points += 10
        game5 = True
    if CORRECT_BRACKET.game6 not in TEAMS or bracket.game6 == CORRECT_BRACKET.game6:
        max_points += 10
        game6 = True
    if CORRECT_BRACKET.game7 not in TEAMS or bracket.game7 == CORRECT_BRACKET.game7:
        max_points += 10
        game7 = True
    if CORRECT_BRACKET.game8 not in TEAMS or bracket.game8 == CORRECT_BRACKET.game8:
        max_points += 10
        game8 = True

    print(max_points)
    # ROUND 2
    game9 = False
    game10 = False
    game11 = False
    game12 = False

    if ((bracket.game9 == CORRECT_BRACKET.game9) 
        or (CORRECT_BRACKET.game9 not in TEAMS and 
            ((CORRECT_BRACKET.game1 not in TEAMS and bracket.game9 == bracket.game1)
            or (CORRECT_BRACKET.game2 not in TEAMS and bracket.game9 == bracket.game2)
            or (CORRECT_BRACKET.game1 in TEAMS and CORRECT_BRACKET.game1 == bracket.game9)
            or (CORRECT_BRACKET.game2 in TEAMS and CORRECT_BRACKET.game2 == bracket.game9)))):
        max_points += 20
        game9 = True

    if ((bracket.game10 == CORRECT_BRACKET.game10) 
        or (CORRECT_BRACKET.game10 not in TEAMS and 
            ((CORRECT_BRACKET.game3 not in TEAMS and bracket.game10 == bracket.game3)
            or (CORRECT_BRACKET.game4 not in TEAMS and bracket.game10 == bracket.game4)
            or (CORRECT_BRACKET.game3 in TEAMS and CORRECT_BRACKET.game3 == bracket.game10)
            or (CORRECT_BRACKET.game4 in TEAMS and CORRECT_BRACKET.game4 == bracket.game10)))):
        max_points += 20
        game10 = True

    if ((bracket.game11 == CORRECT_BRACKET.game11) 
        or (CORRECT_BRACKET.game11 not in TEAMS and 
            ((CORRECT_BRACKET.game5 not in TEAMS and bracket.game11 == bracket.game5)
            or (CORRECT_BRACKET.game6 not in TEAMS and bracket.game11 == bracket.game6)
            or (CORRECT_BRACKET.game5 in TEAMS and CORRECT_BRACKET.game5 == bracket.game11)
            or (CORRECT_BRACKET.game6 in TEAMS and CORRECT_BRACKET.game6 == bracket.game11)))):
        max_points += 20
        game11 = True

    if ((bracket.game12 == CORRECT_BRACKET.game12) 
        or (CORRECT_BRACKET.game12 not in TEAMS and 
            ((CORRECT_BRACKET.game7 not in TEAMS and bracket.game12 == bracket.game7)
            or (CORRECT_BRACKET.game8 not in TEAMS and bracket.game12 == bracket.game8)
            or (CORRECT_BRACKET.game7 in TEAMS and CORRECT_BRACKET.game7 == bracket.game12)
            or (CORRECT_BRACKET.game8 in TEAMS and CORRECT_BRACKET.game8 == bracket.game12)))):
        max_points += 20
        game12 = True
        # or (bracket.game9 == CORRECT_BRACKET.game1 or bracket.game9 == CORRECT_BRACKET.game2) 
        # or (bracket.game9 == bracket.game1 and CORRECT_BRACKET.game1 not in TEAMS)
        # or (bracket.game9 == bracket.game2 and CORRECT_BRACKET.game2 not in TEAMS)
    # if CORRECT_BRACKET.game9 not in TEAMS and (game1 or game2 or bracket.game9 == CORRECT_BRACKET.game1 or bracket.game9 == CORRECT_BRACKET.game2) or bracket.game9 == CORRECT_BRACKET.game9:
    #     max_points += 20
    #     game9 = True
    # if CORRECT_BRACKET.game10 not in TEAMS and (game3 or game4 or bracket.game10 == CORRECT_BRACKET.game3 or bracket.game10 == CORRECT_BRACKET.game4) or bracket.game10 == CORRECT_BRACKET.game10:
    #     max_points += 20
    #     game10 = True
    # if CORRECT_BRACKET.game11 not in TEAMS and (game5 or game6 or bracket.game11 == CORRECT_BRACKET.game5 or bracket.game11 == CORRECT_BRACKET.game6) or bracket.game11 == CORRECT_BRACKET.game11:
    #     max_points += 20
    #     game11 = True
    # if CORRECT_BRACKET.game12 not in TEAMS and (game7 or game8 or bracket.game12 == CORRECT_BRACKET.game7 or bracket.game12 == CORRECT_BRACKET.game8) or bracket.game12 == CORRECT_BRACKET.game12:
    #     max_points += 20
    #     game12 = True
    print(max_points)

    # ROUND 3
    game13 = False
    game14 = False

    if ((bracket.game13 == CORRECT_BRACKET.game13)
        or (CORRECT_BRACKET.game13 not in TEAMS and 
            (game9 and bracket.game9 == bracket.game13
            or game10 and bracket.game10 == bracket.game13))):
        max_points += 40
        game13 = True
    
    if ((bracket.game14 == CORRECT_BRACKET.game14)
        or (CORRECT_BRACKET.game14 not in TEAMS and 
            ((game11 and bracket.game11 == bracket.game14)
            or (game12 and bracket.game12 == bracket.game14)))):
        max_points += 40
        game14 = True
    # if CORRECT_BRACKET.game13 not in TEAMS and (game9 or game10 or bracket.game13 == CORRECT_BRACKET.game9 or bracket.game13 == CORRECT_BRACKET.game10) or bracket.game13 == CORRECT_BRACKET.game13:
    #     max_points += 40
    #     game13 = True
    # if CORRECT_BRACKET.game14 not in TEAMS and (game11 or game12 or bracket.game14 == CORRECT_BRACKET.game11 or bracket.game14 == CORRECT_BRACKET.game12) or bracket.game14 == CORRECT_BRACKET.game14:
    #     max_points += 40
    #     game14 = True

    # WINNER
    if ((bracket.game15 == CORRECT_BRACKET.game15)
    or (CORRECT_BRACKET.game15 not in TEAMS and
        ((game13 and bracket.game13 == bracket.game15)
        or (game14 and bracket.game14 == bracket.game15)))):
        max_points += 80
    # if CORRECT_BRACKET.game15 not in TEAMS and (game13 or game14 or bracket.game15 == CORRECT_BRACKET.game13 or bracket.game15 == CORRECT_BRACKET.game14) or bracket.game15 == CORRECT_BRACKET.game15:
    #     max_points += 80

    return max_points
