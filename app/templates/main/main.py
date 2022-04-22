import datetime
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import User, Post, Comment, Like

main = Blueprint('main', __name__)

@main.route('/index', methods=('GET', 'POST'))
@login_required
def home():
    year = datetime.date.today().year
    posts = current_user.get_post_feed()
    songs = current_user.get_song_feed()
    users = User
    return render_template('main/index.html', posts=posts, songs=songs, users=users, year=year)
