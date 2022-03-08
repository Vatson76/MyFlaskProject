from flask import (
    Blueprint, request, redirect, url_for, flash, render_template,
    session, g
)

api = Blueprint(
    'api',
    __name__,
    template_folder='templates',
    static_folder='static'
)


db = None


@api.before_request
def before_request():
    global db
    db = g.get('link_db')


@api.route('/users')
def user_posts():
    pass


@api.route('/posts')
def user_posts():
    pass


@api.route('/user_posts')
def user_posts():
    pass


@api.route('/user_profile')
def user_posts():
    pass


