from flask import (
    Flask, render_template, url_for, request, flash, session,
    redirect, abort
)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'adsfdafadsfadsfadsf'

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


@app.errorhandler(404)
def pageNotFound(error):
    return render_template(
        'page404.html',
        title='Страница не найдена',
        menu=menu
    ), 404


@app.route('/')
def index():
    print(url_for('index'))
    return render_template(
        'index.html',
        title='Про Flask',
        menu=menu
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
        menu=menu
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
    return render_template('login.html', title='Авторизация', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    print(url_for('about'))
    return f"Пользователь: {username}"


if __name__ == '__main__':
    app.run()
