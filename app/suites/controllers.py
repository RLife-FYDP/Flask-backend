from flask import Blueprint, json

from app.models import Suite, Task, SuiteSchema, TaskSchema

# Define the blueprint: 'suites', set its url prefix: app.url/suites
suites = Blueprint('suites', __name__, url_prefix='/suites')


@suites.route('/')
def get_all_suites():
    suites = Suite.query.all()
    suites_schema = SuiteSchema(many=True)
    return json.dumps(suites_schema.dump(suites))


@suites.route('/<int:id>')
def get_suite(id):
    suite = Suite.query.get(id)
    suite_schema = SuiteSchema()
    return suite_schema.dump(suite)


@suites.route('/<int:id>/tasks')
def get_suite_tasks(id):
    suite = Suite.query.get(id)
    tasks = Task.query.filter(Task.id.in_([user.id for user in suite.users])).all()
    task_schema = TaskSchema(many=True)
    return json.dumps(task_schema.dump(tasks))
