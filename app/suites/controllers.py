from flask import Blueprint, json, jsonify

from app.models import Suite, Task, SuiteSchema, TaskSchema, Assignment

# Define the blueprint: 'suites', set its url prefix: app.url/suites
suites = Blueprint('suites', __name__, url_prefix='/suites')


@suites.route('/')
def get_all_suites():
    suites = Suite.query.all()
    suites_schema = SuiteSchema(many=True)
    return jsonify(json.dumps(suites_schema.dump(suites)))


@suites.route('/<int:id>')
def get_suite(id):
    suite = Suite.query.get(id)
    suite_schema = SuiteSchema()
    return jsonify(suite_schema.dump(suite))


@suites.route('/<int:id>/tasks')
def get_suite_tasks(id):
    suite = Suite.query.get(id)
    assignments = Assignment.query.filter(Assignment.user_id.in_([user.id for user in suite.users])).all()
    unique_task_ids = {assignment.task_id for assignment in assignments}
    tasks = Task.query.filter(Task.id.in_(unique_task_ids)).all()
    task_schema = TaskSchema(many=True)
    return jsonify(json.dumps(task_schema.dump(tasks)))
