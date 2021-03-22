from website import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# class Bracket(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(30), nullable=False)
#     year = db.Column(db.String(5), nullable=False)