from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


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


@app.route('/profile/<username>/<int:user_id>/<path:any_path>')
def profile(username, user_id, any_path):
    print(url_for('about'))
    return f"Пользователь: {username} с id = {user_id}, перешел по пути {any_path}"


@app.route('/contact', methods=["POST", "GET"])
def contact():  # put application's code here

    if request.method == "POST":
        print(request.form)

    return render_template(
        'contact.html',
        title="Обратная связь",
        menu=menu
    )


if __name__ == '__main__':
    app.run()
