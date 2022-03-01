from flask import (
    Flask, render_template, url_for, request, flash, session,
    redirect, abort, make_response
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from FDataBase import FDataBase
from user_login import UserLogin
from settings import get_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adsfdafadsfadsfadsf'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, connect_to_db_and_return_its_translator_class())


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
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        dbase = connect_to_db_and_return_its_translator_class()
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            remember_me = True if request.form.get('remember_me') else False
            login_user(userlogin, remember=remember_me)
            return redirect(request.args.get('next') or url_for('profile'))

        flash("Неверная пара логин/пароль", "error")

    return render_template(
        "login.html",
        menu=get_menu(),
        title="Авторизация"
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
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
    <p>user info: {current_user.get_id()}"""


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
@login_required
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
