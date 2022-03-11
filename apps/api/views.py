from flask import (
    Blueprint, jsonify, request, Response
)
from apps.base.models import *

from flask_marshmallow import Marshmallow


api = Blueprint(
    'api',
    __name__,
    template_folder='templates',
    static_folder='static'
)

ma = Marshmallow(api)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'email',
            'date',
        )


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profiles


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Posts


@api.route('/users')
def users():
    users = Users.query.all()
    user_schema = UserSchema(many=True)
    response = user_schema.dump(users)
    return jsonify({'user': response})


@api.route('/posts')
def posts():
    posts = Posts.query.all()
    posts_schema = PostSchema(many=True)
    response = posts_schema.dump(posts)
    return jsonify({'user': response})


@api.route('/profiles')
def users_profiles():
    profiles = Profiles.query.all()
    profiles_schema = ProfileSchema(many=True)
    response = profiles_schema.dump(profiles)
    return jsonify({'profiles': response})


@api.route('/user_posts/<int:user_id>')
def user_posts(user_id):
    user_posts = Posts.query.filter_by(user_id=user_id).all()
    profiles_schema = PostSchema(many=True)
    response = profiles_schema.dump(user_posts)
    return jsonify({'profiles': response})


@api.route('/user_profile/<int:user_id>')
def users_profile(user_id):
    user_profile = Profiles.query.filter_by(user_id=user_id).first()
    profiles_schema = ProfileSchema()
    response = profiles_schema.dump(user_profile)
    return jsonify({'profiles': response})


@api.route('/post/<int:user_id>', methods=["POST"])
def create_post(user_id):
    if request.method == 'POST':
        data = request.get_json()
        post = Posts(
            title=data['title'],
            text=data['title'],
            url=data['title'],
            user_id=user_id
        )
        try:
            db.session.add(post)
            db.session.flush()
            db.session.commit()
        except Exception as e:
            return Response("An error occurred", status=400)
        return jsonify(PostSchema().dump(post)), 201
