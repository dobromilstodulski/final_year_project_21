from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song, Comment, Favorite
import app.models
from timeago import format
from app import re
from app.utils import allowed_file, make_unique, upload_file, delete_file
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
                result = eval(re.recognize_by_file(audio_file.filename, 0))
                if result['status']['msg'] == 'No result':
                    if artwork_file and audio_file and allowed_file(artwork_file.filename) and allowed_file(audio_file.filename):
                        unique_artwork_filename = make_unique(artwork_file.filename)
                        unique_audio_filename = make_unique(audio_file.filename)
                        artwork_file.filename = secure_filename(unique_artwork_filename)
                        audio_file.filename = secure_filename(unique_audio_filename)
                        upload_file(artwork_file)
                        upload_file(audio_file)
                        Song.create(user=current_user.id,
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
                else:
                    flash('This song is copyrighted!', 'error')
                    return redirect(url_for('song.song_feed'))
                

@song.route('/edit_song/<int:song_id>', methods=('GET', 'POST'))
def edit_song(song_id):
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
                result = eval(re.recognize_by_file(audio_file.filename, 0))
                if result['status']['msg'] == 'No result':
                    if artwork_file and audio_file and allowed_file(artwork_file.filename) and allowed_file(audio_file.filename):
                        unique_artwork_filename = make_unique(artwork_file.filename)
                        unique_audio_filename = make_unique(audio_file.filename)
                        artwork_file.filename = secure_filename(unique_artwork_filename)
                        audio_file.filename = secure_filename(unique_audio_filename)
                        upload_file(artwork_file)
                        upload_file(audio_file)
                        Song.update(artist=artist,
                                    title=title,
                                    feature=featuring,
                                    genre=genre,
                                    tags=tags,
                                    description=description,
                                    artwork=artwork_file.filename,
                                    source=audio_file.filename).where(Song.id == song_id).execute()
                        flash('Upload Succeeded!', 'success')
                        return redirect(url_for('song.song_feed'))
                    else:
                        flash('This song is copyrighted!', 'error')
                        return redirect(url_for('song.song_feed'))
                    

@song.route('/delete_song/<int:song_id>', methods=('GET', 'POST'))
def delete_song(song_id):
    delete_file(Song.get(Song.id == song_id).artwork)
    delete_file(Song.get(Song.id == song_id).source)
    Song.delete().where(Song.id == song_id).execute()
    flash('Song deleted!', 'success')
    return redirect(url_for('song.song_feed'))


@song.route('/song/<int:song_id>', methods=['GET', 'POST'])
def view_post(song_id):
    songs = Song.select().where(Song.id == song_id)
    numberOfComments = songs[0].numComments
    comments = Comment.select().where(Comment.song_id == song_id)
    if request.method == 'POST':
        content = request.form.get('content')

        if content == '':
            flash('Please fill out all the values!', 'warning')

        else:
            Comment.create(
                user_id=current_user.id,
                song_id=song_id,
                comment=content
            )

            Song.update(
                numComments=numberOfComments + 1
            ).where(
                Song.id == song_id
            ).execute()

            flash("Comment Posted!", "success")
            return redirect(request.referrer)

    if songs.count() == 0:
        abort(0)
    return render_template('feed/song.html', songs=songs, format=format, comments=comments)


@song.route('/favorite/<int:song_id>')
@login_required
def like_post(song_id):
    songs = Song.select().where(Song.id == song_id)
    song = songs[0]
    numberOfFavorites = song.numFavorites

    Favorite.create(
        user_id=current_user.id,
        song_id=song.id
    )

    Song.update(
        numFavorites=numberOfFavorites + 1
    ).where(
        Song.id == song.id
    ).execute()
    return render_template('/partials/favorite-section.html', song=song)


@song.route('/unfavorite/<int:song_id>')
@login_required
def unlike_post(song_id):
    songs = Song.select().where(Song.id == song_id)
    song = songs[0]
    numberOfFavorites = song.numFavorites

    Favorite.get(
        user_id=current_user.id,
        song_id=song.id
    ).delete_instance()

    Song.update(
        numFavorites=numberOfFavorites - 1
    ).where(
        Song.id == song.id
    ).execute()
    return render_template('/partials/favorite-section.html', song=song)