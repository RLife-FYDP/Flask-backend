from flask import Blueprint, json

from app.models import User, UserSchema

# Define the blueprint: 'users', set its url prefix: app.url/users
users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def get_all_users():
    users = User.query.all()
    users_schema = UserSchema(many=True)
    return json.dumps(users_schema.dump(users))


@users.route('/<int:id>')
def get_user(id):
    user = User.query.get(id)
    user_schema = UserSchema()
    return user_schema.dump(user)