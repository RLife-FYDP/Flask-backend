import datetime

from marshmallow import ValidationError
from flask import Blueprint, jsonify, request
from app import db
from app.auth.middleware import authorize

from app.models import Task, TaskSchema, Assignment, User

# Define the blueprint: 'suites', set its url prefix: app.url/suites
tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

task_schema = TaskSchema()


@tasks.route('create', methods=['POST'])
@authorize
def create_tasks(user):
    json_data = request.get_json()
    try:
        task_data = task_schema.load(json_data)
    except ValidationError as err:
        return {"message": "Bad post body", "errors": str(err)}, 400

    task = Task(
        title=task_data['title'],
        description=task_data['description'],
        tags=task_data['tags'],
        points=task_data['points'],
        start_time=task_data.get('startTime', datetime.datetime.now()),
        last_completed=task_data.get('lastCompleted'),
        rrule_option=task_data.get('rruleOption'),
    )
    for user_id in task_data['assignee']:
        user = User.query.get(user_id)
        task.assignments.append(
            Assignment(user=user, task=task, completed_at=None)
        )
    db.session.add(task)
    db.session.commit()
    return jsonify(task=task_schema.dump(task))


@tasks.route('/<int:id>', methods=['PUT'])
@authorize
def update_task(user, id):
    try:
        task_data = task_schema.load(request.get_json())
    except ValidationError as err:
        return {"message": "Bad post body", "errors": str(err)}, 400
    task = Task.query.get_or_404(id)
    task.title = task_data['title']
    task.description = task_data['description'],
    task.tags = task_data['tags'],
    task.points = task_data['points'],
    task.start_time = task_data['startTime']
    task.last_completed = task_data.get('lastCompleted'),
    task.rrule_option = task_data['rruleOption'],
    task.updated_at = datetime.datetime.now()
    try:
        db.session.commit()
        return task_data
    except Exception as err:
        return {"message": "Error updating", "errors": str(err)}, 400


@tasks.route('/<int:id>', methods=['DELETE'])
@authorize
def delete_task(user, id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return {"message": f"task {id} deleted"}, 200
    except Exception as err:
        return {"message": f"Error delete record {id}", "errors": str(err)}, 500
