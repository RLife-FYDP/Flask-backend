from flask import Blueprint
from app.models import User, UserSchema
from sqlalchemy import asc

# Define the blueprint: 'matches', set its url prefix: app.url/matches
#matches = Blueprint('matches', __name__, url_prefix='/matches')

def getRating(id):
   #first get my own rating 
   userRating = User.query.get(id).rating
   print(userRating)
   return

def findMatches(rating):
   potentialMatches = []
   #get top 10 closest users from database 
   topMatches = User.query.order_by(asc(User.rating-rating)).limit(10).all()
   user_schema = UserSchema(many=True, exclude=['password_digest'])
   print(user_schema.dump(topMatches))


rating = getRating(4)
b = findMatches(rating)
