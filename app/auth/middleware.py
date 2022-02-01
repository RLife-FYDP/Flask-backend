from functools import wraps
from flask import abort, request
from app.models import User

from app.utils.auth import decode_access_token

def authorize(f):
  @wraps(f)
  def decorated_function(*args, **kws):
    if not 'Authorization' in request.headers:
      abort(401)

    user = None
    data = request.headers['Authorization']
    token = data.replace('Bearer ', '')
    try:
      decoded_token = decode_access_token(token)
      user = User.query.get(decoded_token['user_id'])

    except:
      abort(401)

    return f(user, *args, **kws)            
  return decorated_function