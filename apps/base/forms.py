from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField(
        "Пароль: ",
        validators=[
            DataRequired(),
            Length(min=4, max=100, message="Пароль должен содержать от 4 до 100 символов")
        ]
    )
    remember_me = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField(
        "Имя: ",
        validators=[Length(min=4, max=100, message="Имя должно содержать от 4 до 100 символов")]
    )
    age = IntegerField(
        "Возраст: ",
        validators=[
            NumberRange(
                min=12,
                max=150,
                message="Вам должно быть от 12 до 150 лет, чтобы зарегистрироваться на сайте"
            )
        ]
    )
    city = StringField(
        "Город: ",
        validators=[Length(min=4, max=100, message="Город должен содержать от 4 до 100 символов")]
    )
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField(
        "Пароль: ",
        validators=[
            DataRequired(),
            Length(min=4, max=100, message="Пароль должен содержать от 4 до 100 символов")
        ]
    )
    password2 = PasswordField(
        "Повторите пароль: ",
        validators=[
            DataRequired(),
            EqualTo('password', message='Пароли не совпадают')
        ]
    )
    submit = SubmitField("Регистрация")


class AddPostForm(FlaskForm):
    title = StringField(
        "Название: ",
        validators=[Length(min=4, max=100, message="Название должно содержать от 4 до 100 символов")]
    )
    text = TextAreaField(
        "Текст: ",
        validators=[Length(min=4, max=500, message="Размер текста должен быть от 4 до 100 символов")]
    )
    url = StringField(
        "URL статьи: ",
        validators=[Length(min=4, max=50, message="URL должен быть от 4 до 100 символов")]
    )

    submit = SubmitField("Добавить")
