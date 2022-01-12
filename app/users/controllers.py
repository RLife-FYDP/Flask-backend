from flask import Blueprint, jsonify

from app.models import User, UserSchema, TaskSchema

# Define the blueprint: 'users', set its url prefix: app.url/users
users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def get_all_users():
    users = User.query.all()
    users_schema = UserSchema(many=True, exclude=['password_digest'])
    return jsonify(users_schema.dump(users))


@users.route('/<int:id>')
def get_user(id):
    user = User.query.get(id)
    user_schema = UserSchema(exclude=['password_digest'])
    return jsonify(user_schema.dump(user))


@users.route('/<int:id>/tasks')
def get_user_tasks(id):
    user = User.query.get(id)
    tasks = user.tasks
    task_schema = TaskSchema(many=True)
    return jsonify(task_schema.dump(tasks))
