from app import socketio, db
from flask_socketio import join_room, leave_room, emit
from app.models import SuiteMessage, SuiteMessageSchema

suite_message_schema = SuiteMessageSchema()

@socketio.on('join_room')
def handle_join_room(suite_id: int):
  join_room(str(suite_id))
  print('joined room')

@socketio.on('send_message')
def handle_send_message(data):
  from_user_id = data['from']
  room = data['suite_id']
  content = data['message']
  message = SuiteMessage(
    from_user=from_user_id,
    content=content,
    suite_id=room
  )
  db.session.add(message)
  db.session.commit()
  emit('emit_message', suite_message_schema.dump(message), room=str(room))

@socketio.on('send_dm_message')
def handle_send_dm_message(data):
  print(data)
  from_user_id = data['from']
  to_user_id = data['to']
  room = data['suite_id']
  encrypted_message = data['encrypted_message']
  message = {
    'from_user':from_user_id,
    'to_user': to_user_id,
    'encrypted_message':encrypted_message,
    'suite_id':room
  }
  emit('emit_dm_message', message, room=str(room))

