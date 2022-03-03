from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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
