from flask import (
    Flask, render_template, url_for, request, flash, session,
    redirect, abort
)
from settings import get_db
from FDataBase import FDataBase


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
    return render_template(
        'index.html',
        title='Про Flask',
        menu=get_menu(),
        posts=get_posts()
    )


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


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    print(url_for('about'))
    return f"Пользователь: {username}"


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    dbase = connect_to_db_and_return_its_translator_class

    if request.method == "POST":
        name_data = request.form['name']
        post_data = request.form['post']
        if len(name_data) > 4 and len(post_data) > 10:
            res = dbase.addPost(name_data, post_data)
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


@app.route('/post/<int:post_id>', methods=['GET'])
def showPost(post_id):
    dbase = connect_to_db_and_return_its_translator_class()
    title, post = dbase.getPost(post_id)
    if not title:
        abort(404)

    return render_template(
        'post.html',
        menu=get_menu(),
        title=title,
        post=post
    )


if __name__ == '__main__':
    app.run()
