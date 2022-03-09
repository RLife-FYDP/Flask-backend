import datetime

from flask import Blueprint, jsonify, request
from app.auth.middleware import authorize
from app import db
from app.utils.constants import CANVAS_BLOB
from app.models import Suite, Task, SuiteSchema, TaskSchema, Assignment, User, UserSchema

# Define the blueprint: 'suites', set its url prefix: app.url/suites
suites = Blueprint('suites', __name__, url_prefix='/suites')


@suites.route('/', methods=['GET'])
def get_all_suites():
    suites = Suite.query.all()
    suites_schema = SuiteSchema(many=True)
    return jsonify(suites_schema.dump(suites))

@suites.route('/create', methods=['POST'])
@authorize
def create_suite(user):
    body = request.get_json()
    print(body)
    suite = Suite(
        active=True,
        canvas=CANVAS_BLOB,
        name=body['name'],
        address=body['address'],
        messages=[]
    )
    db.session.add(suite)

    # add users to suite
    for roommate in body['users']:
        if 'userId' in roommate:
            user = User.query.get(roommate['userId'])
            user.suite_id = suite.id
        elif 'email' in roommate:
            user = User.query.filter_by(email=roommate['email']).first()
            if user != None:
                user.suite_id = suite.id

    db.session.commit()
    suite_schema = SuiteSchema()
    return jsonify(suite_schema.dump(suite))

@suites.route('/<int:id>')
def get_suite(id):
    suite = Suite.query.get(id)
    suite_schema = SuiteSchema()
    return jsonify(suite_schema.dump(suite))


@suites.route('/<int:id>/tasks')
@authorize
def get_suite_tasks(user, id):
    suite = Suite.query.get(id)
    assignments = Assignment.query.filter(Assignment.user_id.in_([user.id for user in suite.users])).all()
    unique_task_ids = {assignment.task_id for assignment in assignments}
    tasks = Task.query.filter(Task.id.in_(unique_task_ids)).all()
    task_schema = TaskSchema(many=True)
    return jsonify(task_schema.dump(tasks))


@suites.route('/<int:id>/users')
def get_suite_users(id):
    suite = Suite.query.get(id)
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(suite.users))


@suites.route('/<int:id>/update_canvas', methods=['PUT'])
@authorize
def update_canvas(user, id):
    request_data = request.get_json()
    suite = Suite.query.get(id)
    suite.canvas = request_data['canvas']
    suite.updated_at = datetime.datetime.now()
    try:
        db.session.commit()
        return {"message": "updated canvas"}, 200
    except Exception as err:
        return {"message": "Error updating", "errors": str(err)}, 400
