from flask import Blueprint
from app.models import User
from app import login_manager

song = Blueprint('song', __name__)

@song.route('/song_feed')
def post_feed():
    return 'song_feed'