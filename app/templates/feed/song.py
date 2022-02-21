from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song, database
import app.models
from app import login_manager

song = Blueprint('song', __name__)


@login_manager.user_loader
def load_user(id):
    try:
        return User.get(User.id == id)
    except app.models.DoesNotExist:
        return None


@song.before_request
def before_request():
    """Connect to database before each request
            g is a global object, passed around all time in flask, used to setup things which
            we wanna have available everywhere.
    """
    g.db = database
    g.db.connect()
    g.user = current_user


@song.route('/song_feed')
def song_feed():
    return render_template('feed/song_feed.html', songs=Song)


@song.route('/new_song', methods=('GET', 'POST'))
@login_required
def post():
    if request.method == 'POST':
        artist = request.form.get('artist')
        title = request.form.get('title')
        featuring = request.form.get('featuring')
        genre = request.form.get('genre')
        tags = request.form.get('tags')
        description = request.form.get('description')
        artwork = request.form.get('artwork')
        audio = request.form.get('audio')

        if artist == '' or title == '' or genre == '' or artwork == '' or audio == '':
            flash('Please fill out all the values!', 'warning')

        else:
            Song.create(user=g.user._get_current_object(),
                        artist=artist,
                        title=title,
                        feature=featuring,
                        genre=genre,
                        tags=tags,
                        description=description,
                        artwork=artwork,
                        source=audio)
        flash("Song Uploaded!", "success")
        return redirect(url_for('song.song_feed'))
    return render_template('feed/song_feed.html')
