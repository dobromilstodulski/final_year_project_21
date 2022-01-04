from flask import Blueprint
from app.models import User
from app import login_manager

song = Blueprint('song', __name__)

@login_manager.user_loader
def load_user(user_id): #reload user object from the user ID stored in the session
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@song.route('/song_feed')
def post_feed():
    return 'song_feed'