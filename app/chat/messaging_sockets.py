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
  print('sent message')
  print(from_user_id)
  emit('emit_message', suite_message_schema.dump(message), room=str(room))

