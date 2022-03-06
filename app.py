from flask import (
    Flask, render_template, url_for, request, flash, session,
    redirect, abort, make_response, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from FDataBase import FDataBase
from user_login import UserLogin
from settings import get_db
from forms import LoginForm, RegisterForm
from admin.admin import admin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'adsfdafadsfadsfadsf'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'

app.register_blueprint(admin, url_prefix='/admin')


dbase: FDataBase


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template(
        'page404.html',
        title='Страница не найдена',
        menu=dbase.getMenu()
    ), 404


@app.route('/')
def index():
    content = render_template(
        'index.html',
        title='Про Flask',
        menu=dbase.getMenu(),
        posts=dbase.getPosts()
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
        menu=dbase.getMenu(),
    )


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            remember_me = form.remember_me.data
            login_user(userlogin, remember=remember_me)
            return redirect(request.args.get('next') or url_for('profile'))

        flash("Неверная пара логин/пароль", "error")

    return render_template(
        "login.html",
        menu=dbase.getMenu(),
        title="Авторизация",
        form=form
    )


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password1 = form.password.data

        password_hash = generate_password_hash(password1)
        res = dbase.addUser(username, email, password_hash)
        if res:
            flash("Вы успешно зарегистрированы", 'success')
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", 'error')

    return render_template(
        "register.html",
        menu=dbase.getMenu(),
        title="Регистрация",
        form=form
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
    return render_template(
        'profile.html',
        menu=dbase.getMenu(),
        title='Профиль пользователя'
    )


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    response = make_response(img)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():

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
        menu=dbase.getMenu(),
        title='Добавление статьи'
        )


@app.route('/post/<alias>', methods=['GET'])
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template(
        'post.html',
        menu=dbase.getMenu(),
        title=title,
        post=post
    )


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", 'error')

    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run()
