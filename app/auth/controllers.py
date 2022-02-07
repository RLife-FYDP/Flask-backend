from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate

from jwt.exceptions import InvalidSignatureError
from sqlalchemy.exc import NoResultFound
from app.models import User, UserSchema
from app import db
from app.utils.auth import hash_password, verify_password, create_access_token, create_refresh_token, \
    decode_refresh_token

# Define the blueprint: 'users', set its url prefix: app.url/users
auth = Blueprint('auth', __name__, url_prefix='/auth')


class UserRegisterBodySchema(Schema):
    first_name = fields.String(required=True,
                               validate=[validate.Length(min=2, max=20), validate.Regexp(r'^[a-zA-Z-\s]+$')])
    last_name = fields.String(required=True,
                              validate=[validate.Length(min=2, max=20), validate.Regexp(r'^[a-zA-Z-\s]+$')])
    email = fields.String(required=True, validate=validate.Email())
    age = fields.Number(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(['Male', 'Female', 'Non-binary']))
    password = fields.String(required=True, validate=validate.Length(min=8, max=50))


class UserLoginBodySchema(Schema):
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=8, max=50))


user_register_body_schema = UserRegisterBodySchema()
user_login_body_schema = UserLoginBodySchema()
user_schema = UserSchema(exclude=['password_digest'])


@auth.route('/register', methods=['POST'])
def create_user():
    json_data = request.get_json()
    try:
        user_data = user_register_body_schema.load(json_data)
    except ValidationError as err:
        return {"message": "Bad post body", "errors": str(err)}, 400
    # check for user already exists
    users = User.query.filter(User.email == user_data['email']).all()
    if len(users) > 0:
        return {"message": f'User with email {user_data["email"]} already exists'}

    # generate password digest
    password_digest = hash_password(user_data['password'])

    # create user in database
    user = User(
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        age=user_data['age'],
        gender=user_data['gender'],
        password_digest=password_digest,
        rating=-1,
        suite_id=4
        # TODO: so troll dump all the new boys in suite 4 so they at least have a suite so we can test the app
    )
    db.session.add(user)
    db.session.commit()

    # create tokens
    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})
    return jsonify(user=user_schema.dump(user), access_token=access_token, refresh_token=refresh_token)


@auth.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    try:
        user_data = user_login_body_schema.load(json_data)
    except ValidationError as err:
        return {"message": "Bad post body", "errors": str(err)}, 400
    try:
        user = User.query.filter(User.email == user_data['email']).one()
    except NoResultFound as err:
        return {"message": "Invalid username/password"}, 404

    if not verify_password(user_data['password'], user.password_digest):
        return {"message": "Invalid username/password"}, 404
    # create tokens
    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})
    return jsonify(user=user_schema.dump(user), access_token=access_token, refresh_token=refresh_token)


@auth.route('/refresh', methods=['POST'])
def refresh_token():
    json_data = request.get_json()
    if 'refresh_token' not in json_data:
        return {"message": "'refresh_token' missing from request body"}, 404
    try:
        decoded_token = decode_refresh_token(json_data['refresh_token'])
    except InvalidSignatureError:
        return {"message": "Invalid token"}, 401
    try:
        user = User.query.get(decoded_token['user_id'])
    except NoResultFound as err:
        return {"message": "Invalid token"}, 401
    access_token = create_access_token({"user_id": user.id})
    # TODO: revoke the refresh token after use
    return {"access_token": access_token}, 200


@auth.route('/revoke')
def revoke_token():
    # TODO
    return {}, 200