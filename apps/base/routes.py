from flask import (
    render_template, url_for, request, flash, redirect, abort, make_response, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from apps.base.user_login import UserLogin
from apps.base.forms import LoginForm, RegisterForm, AddPostForm

from apps.settings import app, db, login_manager

from apps.base.models import MenuElements, Users, Posts, Profiles

menu = MenuElements.query.all()
posts = Posts.query.all()


def link_db():
    if not hasattr(g, 'link_db'):
        g.link_db = db
    return g.link_db


@app.before_request
def before_request():
    link_db()


user_login_instance = UserLogin(user_model=Users, profile_model=Profiles)


@login_manager.user_loader
def load_user(user_id):
    return user_login_instance.fromDB(user_id)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template(
        'base_templates/page404.html',
        title='Страница не найдена',
        menu=menu
    ), 404


@app.route('/')
def index():
    content = render_template(
        'base_templates/index.html',
        title='Про Flask',
        menu=menu,
        posts=posts
    )
    res = make_response(content)
    res.headers['Content-Type'] = 'text/html'
    res.headers['Server'] = 'flasksite'
    return res


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('base_templates/about.html')


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка отправки')

    return render_template(
        'base_templates/contact.html',
        title="Обратная связь",
        menu=menu,
    )


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            userlogin = user_login_instance.create(user)
            remember_me = form.remember_me.data
            login_user(userlogin, remember=remember_me)
            return redirect(request.args.get('next') or url_for('profile'))

        flash("Неверная пара логин/пароль", "error")

    return render_template(
        "base_templates/login.html",
        menu=menu,
        title="Авторизация",
        form=form
    )


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            password_hash = generate_password_hash(form.password.data)
            user = Users(email=form.email.data, password=password_hash)

            db.session.add(user)
            db.session.flush()

            user_profile = Profiles(
                name=form.name.data,
                age=form.age.data,
                city=form.city.data,
                user_id=user.id,
            )

            db.session.add(user_profile)
            db.session.commit()

            flash("Вы успешно зарегистрированы", 'success')

            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash("Ошибка при добавлении в БД", 'error')

    return render_template(
        "base_templates/register.html",
        menu=menu,
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
        'base_templates/profile.html',
        menu=menu,
        title='Профиль пользователя',
    )


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app, Profiles)
    if not img:
        return ""

    response = make_response(img)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    form = AddPostForm()

    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data
            url = form.url.data

            if len(title) > 4 and len(text) > 10:
                try:
                    post = Posts(
                        title=title,
                        text=text,
                        url=url,
                        user_id=current_user.get_id()
                    )
                    db.session.add(post)
                    db.session.flush()
                    db.session.commit()
                    flash('Статья добавлена успешно', category='success')
                except Exception as e:
                    db.session.rollback()
                    flash('Ошибка при добавлении статьи', category='error')

    return render_template(
        'base_templates/add_post.html',
        menu=menu,
        title='Добавление статьи',
        form=form
        )


@app.route('/post/<alias>', methods=['GET'])
@login_required
def showPost(alias):
    post = Posts.query.filter(Posts.url.ilike(f"{alias}")).first()
    title = post.title
    if not title:
        abort(404)

    return render_template(
        'base_templates/post.html',
        menu=menu,
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
                Profiles.query.filter_by(
                    user_id=current_user.get_id()
                ).update(dict(avatar=img))
                db.session.commit()
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                db.session.rollback()
                flash("Ошибка обновления аватара", 'error')

    return redirect(url_for('profile'))