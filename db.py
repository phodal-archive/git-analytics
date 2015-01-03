import sqlite3

from flask import Flask, g, app


app = Flask(__name__)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect("dev.db")
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def post_story(args):
    db = get_db()
    db.execute(
        'insert into pair (story_type, story_number, story_description, story_title, user, story_day) values (?, ?, ?, ?, ?, ?)',
        [args["story_type"], args["story_number"], args["story_description"], args["story_title"], args["user"],
         args["story_day"]])
    db.commit()