import sqlite3
import os
from flask import Flask, render_template, request, g

DATABASE = '/tmp/flask_site.db'
DEBUG = True
SECRET_KEY = 'asdfadfasdfadfgadsfgfadf'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask_site.db ')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db
