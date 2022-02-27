from flask import (
    Flask, render_template, url_for, request, flash, session,
    redirect, abort, make_response
)
from werkzeug.security import generate_password_hash

from FDataBase import FDataBase
from settings import get_db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'adsfdafadsfadsfadsf'

# menu = [
#     {"name": "Установка", "url": "install-flask"},
#     {"name": "Первое приложение", "url": "first-app"},
#     {"name": "Обратная связь", "url": "contact"},
# ]


def connect_to_db_and_return_its_translator_class():
    db = get_db()
    return FDataBase(db)


@app.before_request
def before_request():
    print('before_request() called')


def get_menu():
    dbase = connect_to_db_and_return_its_translator_class()
    return dbase.getMenu()


def get_posts():
    dbase = connect_to_db_and_return_its_translator_class()
    return dbase.getPosts()


@app.errorhandler(404)
def pageNotFound(error):
    return render_template(
        'page404.html',
        title='Страница не найдена',
        menu=get_menu()
    ), 404


@app.route('/')
def index():
    content = render_template(
        'index.html',
        title='Про Flask',
        menu=get_menu(),
        posts=get_posts()
    )
    res = make_response(content)
    res.headers['Content-Type'] = 'text/html'
    res.headers['Server'] = 'flasksite'
    return res


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html')


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка отправки')

    return render_template(
        'contact.html',
        title="Обратная связь",
        menu=get_menu(),
    )


@app.route('/login', methods=["POST", "GET"])
def login():
    if "userLogged" in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif (
            request.method == 'POST' and
            request.form['username'] == 'selfedu' and
            request.form['psw'] == "123"
    ):
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template(
        'login.html',
        title='Авторизация',
        menu=get_menu()
    )


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        a = request
        dbase = connect_to_db_and_return_its_translator_class()
        username = request.form['username']
        email = request.form['user_email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if (len(username) > 4
                and len(email) > 4 and
                len(password1) > 4
                and password1 == password2):
            password_hash = generate_password_hash(password1)
            res = dbase.addUser(username, email, password_hash)
            if res:
                flash("Вы успешно зарегистрированы", 'success')
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", 'error')
        else:
            flash("Неверно заполнены поля", 'error')

    return render_template(
        "register.html",
        menu=get_menu(),
        title="Регистрация"
    )


@app.route('/logout')
def logout():
    res = make_response(f"<h1>Форма выхода</h1><p>")
    res.set_cookie("logged", "", max_age=0)
    return res


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    print(url_for('about'))
    return f"Пользователь: {username}"


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    dbase = connect_to_db_and_return_its_translator_class()

    if request.method == "POST":

        name_data = request.form['name']
        post_data = request.form['post']
        url_data = request.form['url']

        if len(name_data) > 4 and len(post_data) > 10:
            res = dbase.addPost(name_data, post_data, url_data)
            if not res:
                flash('Ошибка при добавлении статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка при добавлении статьи', category='error')

    return render_template(
        'add_post.html',
        menu=get_menu(),
        title='Добавление статьи'
        )


@app.route('/post/<alias>', methods=['GET'])
def showPost(alias):
    dbase = connect_to_db_and_return_its_translator_class()
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template(
        'post.html',
        menu=get_menu(),
        title=title,
        post=post
    )


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)


if __name__ == '__main__':
    app.run()
