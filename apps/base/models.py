from sqlalchemy.orm import relationship
from apps.settings import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    profile = relationship("Profiles", back_populates="user", uselist=False)
    posts = relationship("Posts", back_populates="user")

    def __repr__(self):
        return 'user: {}'.format(self.id)


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))
    avatar = db.Column(db.LargeBinary())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("Users", back_populates="profile")

    def __repr__(self):
        return 'profile: {}'.format(self.id)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("Users", back_populates="posts")


class MenuElements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(50), nullable=False)
