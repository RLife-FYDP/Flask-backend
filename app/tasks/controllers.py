from itsdangerous import json
from marshmallow import Schema, fields, ValidationError, validate, ValidationError
from flask import Blueprint, jsonify, request
from flask_marshmallow import Schema
import datetime
from app import db


from app.models import Suite, Task, SuiteSchema, TaskSchema, Assignment, UserSchema

# Define the blueprint: 'suites', set its url prefix: app.url/suites
tasks = Blueprint('tasks', __name__, url_prefix='/tasks')


class TaskBodySchema(Schema):
  taskName = fields.String(required=True, validate=[validate.Length(min=2, max=20), validate.Regexp(r'^[a-zA-Z-\s]+$')])
  description = fields.String(required=True, validate=[validate.Length(min=2, max=20), validate.Regexp(r'^[a-zA-Z-\s]+$')])
  #to do: this has to be an array 
  #assignees = fields.String(required=True)
  dueDate = fields.String(required=True)
 
task_body_schema = TaskBodySchema()
task_schema = TaskSchema()

@tasks.route('',methods=['POST'])
def create_tasks():
   print("in create_tasks")
   json_data = request.get_json()
   print("printing taskname: ",json_data['taskName'])

   try:
      task_data = task_body_schema.load(json_data)
   except ValidationError as err:
      return {"message": "Bad post body", "errors": str(err)}, 400

   task = Task(
      title = task_data['taskName'],
      description = task_data['description'],
      due_date = task_data['dueDate'],

      #not implemented
      priority = 0,
      completed = False,
      tags = "",
      points = 0,
      start_time = datetime.datetime.now(),
   )
   db.session.add(task)
   db.session.commit()
   return jsonify(task=task_schema.dump(task))