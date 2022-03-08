from flask import Blueprint, request
from app.auth.middleware import authorize

# Define the blueprint: 'matches', set its url prefix: app.url/matches
signal = Blueprint('signal', __name__, url_prefix='/chat/signal')

pre_key_bundles = {}

@signal.route('/<int:id>/preKeyBundle', methods=['GET'])
@authorize
def get_pre_key_bundle(user, id):
  if id not in pre_key_bundles:
    return {"message": "Pre key bundle not found"}, 404
  bundle = pre_key_bundles[id]
  if len(bundle['oneTimePreKeys']) == 0:
    return {"message": "Out of one time pre keys"}
  oneTimePreKey = bundle['oneTimePreKeys'].pop()
  resBundle = {
    'identityKey': bundle['identityPubKey'],
    'signedPreKey': bundle['signedPreKey'],
    'preKey': oneTimePreKey,
    'registrationId': bundle['registrationId']
  }
  return resBundle, 200

@signal.route('/<int:id>/preKeyBundle', methods=['POST'])
@authorize
def store_pre_key_bundle(user, id):
  bundle = request.get_json()
  pre_key_bundles[id] = bundle
  return {}, 200


