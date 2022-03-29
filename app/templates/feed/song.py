from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song, database
import app.models
from timeago import format
from app import login_manager
from app.utils import allowed_file, make_unique, upload_file
from werkzeug.utils import secure_filename

song = Blueprint('song', __name__)

@song.route('/song_feed')
def song_feed():
    return render_template('feed/song_feed.html', songs=Song, user=User, format=format)


@song.route('/new_song', methods=('GET', 'POST'))
def new_song():
    if request.method == 'POST':
        artist = request.form.get('artist')
        title = request.form.get('title')
        featuring = request.form.get('featuring')
        genre = request.form.get('genre')
        tags = request.form.get('tags')
        description = request.form.get('description')
        artwork_file = request.files["artwork"]
        audio_file = request.files["audio"]
        if "artwork" not in request.files and "audio" not in request.files:
            flash('Missing files! Please upload something!', 'warning')
        if "artwork" in request.files and "audio" in request.files:
            if artwork_file.filename == '' or audio_file.filename == '' or artist == '' or title == '' or genre == '':
                flash('Please fill out all the values!', 'warning')
            else: 
                if artwork_file and audio_file and allowed_file(artwork_file.filename) and allowed_file(audio_file.filename):
                    unique_artwork_filename = make_unique(artwork_file.filename)
                    unique_audio_filename = make_unique(audio_file.filename)
                    artwork_file.filename = secure_filename(unique_artwork_filename)
                    audio_file.filename = secure_filename(unique_audio_filename)
                    upload_file(artwork_file)
                    upload_file(audio_file)
                    Song.create(user=g.user._get_current_object(),
                                artist=artist,
                                title=title,
                                feature=featuring,
                                genre=genre,
                                tags=tags,
                                description=description,
                                artwork=artwork_file.filename,
                                source=audio_file.filename)
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('song.song_feed'))
                else:
                    return redirect("/")
