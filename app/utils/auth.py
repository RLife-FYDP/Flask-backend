import bcrypt
import jwt
import datetime
from app.config import ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET

def hash_password(password: str):
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(password.encode(), salt)

def verify_password(provided_password: str, hashed_password: str):
  return bcrypt.checkpw(provided_password.encode(), hashed_password.encode())

def create_access_token(payload: object):
  payload['exp'] = (datetime.datetime.now() + datetime.timedelta(hours=12)).timestamp()
  return jwt.encode(payload, ACCESS_TOKEN_SECRET)

def create_refresh_token(payload: object):
  payload['exp'] = (datetime.datetime.now() + datetime.timedelta(days=365)).timestamp()
  return jwt.encode(payload, REFRESH_TOKEN_SECRET)

def decode_access_token(token: str):
  return jwt.decode(token, ACCESS_TOKEN_SECRET, "HS256")

def decode_refresh_token(token: str):
  return jwt.decode(token, REFRESH_TOKEN_SECRET, "HS256")