from flask import (
    Blueprint, request, redirect, url_for, flash, render_template,
    session, g
)

admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)


db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


def login_admin():
    session['admin_logged'] = True


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [
    {'url': '.index', 'title': 'Панель'},
    {'url': '.listpubs', 'title': 'Список статей'},
    {'url': '.listusers', 'title': 'Список пользователей'},
    {'url': '.logout', 'title': 'Выйти'},
]


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template(
        'admin/index.html',
        menu=menu,
        title='Админ-панель'
    )


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['password'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверна пара логин/пароль", "error")
    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))

    list_of_pubs = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text , url FROM posts")
            list_of_pubs = cur.fetchall()
        except Exception as e:
            print("Ошибка получения статей из БД" + str(e))

    return render_template(
        'admin/listpubs.html',
        title='Список статей',
        menu=menu,
        list=list_of_pubs
    )

@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    list_of_users = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list_of_users = cur.fetchall()
        except Exception as e:
            print("Ошибка получения пользователей из БД" + str(e))

    return render_template(
        'admin/listusers.html',
        title='Список пользователей',
        menu=menu,
        list=list_of_users
    )
