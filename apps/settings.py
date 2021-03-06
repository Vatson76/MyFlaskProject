from flask import (
    Flask
)
from flask_login import LoginManager
from apps.admin.admin import admin
from apps.api.views import api
from .extensions import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'adsfdafadsfadsfadsf'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_site2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



