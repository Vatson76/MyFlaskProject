from flask import url_for
from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self, profile_model, user_model):
        self.__user_model = user_model
        self.__profile_model = profile_model

    def fromDB(self, user_id):
        self.__user = self.__user_model.query.filter_by(id=user_id).first()
        self.__profile = self.__profile_model.query.filter_by(user_id=user_id).first()
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_profile(self):
        return self.__profile

    def get_id(self):
        return(self.__user.id)

    def getName(self):
        return(self.__profile.name if self.__profile else "Имя не указано")

    def getEmail(self):
        return (self.__user.email if self.__user else "Email не указан")

    def getAvatar(self, app, model_with_avatar):
        img = None
        avatar = self.__profile.avatar
        if not avatar:
            try:
                with app.open_resource(
                        app.root_path + url_for('static', filename='media/default_avatar.png'), "rb"
                ) as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = avatar

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == 'PNG':
            return True
        return False
