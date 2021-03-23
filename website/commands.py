import click
from flask.cli import with_appcontext

from website import db
from website.models import User, Bracket

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()