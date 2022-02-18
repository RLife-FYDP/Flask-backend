from datetime import datetime
from flask import Blueprint, request
import boto3
from app.auth.middleware import authorize

# Define the blueprint: 'users', set its url prefix: app.url/users
media = Blueprint('media', __name__, url_prefix='/media')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

client = boto3.client(
    's3',
    aws_access_key_id='AKIAROMLTNG5OG75E2FM',
    aws_secret_access_key='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',
)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@media.route('/image/upload', methods=['POST'])
@authorize
def post_image(_):
  if 'file' not in request.files:
    return {"message": "Missing file"}, 400
  file = request.files['file']
  if file.filename == '':
    return {"message": "No selected file"}, 400
  if not allowed_file(file.filename):
    return {"message": f'Invalid file extension. Valid extensions are: {ALLOWED_EXTENSIONS}'}, 400
  extension = file.filename.split('.')[-1].lower()
  ts = str(datetime.now().timestamp()).replace('.','-')
  client.upload_fileobj(file, 'rlife', f'{ts}.{extension}', ExtraArgs={'ContentType': f'image/{extension}', 'ACL': 'public-read'})
  return {'url': f'https://rlife.s3.us-east-1.amazonaws.com/{ts}.{extension}'}, 200

