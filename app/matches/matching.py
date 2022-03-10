from flask import Blueprint, jsonify
from app.models import User, UserSchema
from sqlalchemy import asc

# Define the blueprint: 'matches', set its url prefix: app.url/matches
matches = Blueprint('matches', __name__, url_prefix='/matches')

@matches.route('/<int:id>/getRating/')
def getRating(id):
   #grab only your own rating 
   userRating = User.query.get(id).rating
   return jsonify(userRating)

@matches.route('/<int:id>/findMatches')
def findMatches(id):
   rating = User.query.get(id).rating
   #get top 10 closest users from database 
   topMatches = User.query.filter(User.suite_id == None).order_by(asc(User.rating-rating)).all()
   user_schema = UserSchema(many=True, exclude=['password_digest'])
   return jsonify((user_schema.dump(topMatches)))

