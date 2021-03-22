from website import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Bracket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    year = db.Column(db.String(5), nullable=False)
    game1 = db.Column(db.String(30), nullable=False)
    game2 = db.Column(db.String(30), nullable=False)
    game3 = db.Column(db.String(30), nullable=False)
    game4 = db.Column(db.String(30), nullable=False)
    game5 = db.Column(db.String(30), nullable=False)
    game6 = db.Column(db.String(30), nullable=False)
    game7 = db.Column(db.String(30), nullable=False)
    game8 = db.Column(db.String(30), nullable=False)
    game9 = db.Column(db.String(30), nullable=False)
    game10 = db.Column(db.String(30), nullable=False)
    game11 = db.Column(db.String(30), nullable=False)
    game12 = db.Column(db.String(30), nullable=False)
    game13 = db.Column(db.String(30), nullable=False)
    game14 = db.Column(db.String(30), nullable=False)
    game15 = db.Column(db.String(30), nullable=False)
    w_goals = db.Column(db.Integer)
    l_goals = db.Column(db.Integer)