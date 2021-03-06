import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app.models import Song, Comment, Favorite
from app.utils import allowed_file, make_unique, upload_file, delete_file
from werkzeug.utils import secure_filename
import cloudinary.uploader

song = Blueprint('song', __name__)


@song.route('/song/new', methods=('GET', 'POST'))
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
                    artwork_upload_result = cloudinary.uploader.upload(artwork_file, public_id=unique_artwork_filename)
                    audio_upload_result = cloudinary.uploader.upload(audio_file, public_id=unique_artwork_filename, resource_type="video")
                    Song.create(user_id=current_user.id,
                                artist=artist,
                                title=title,
                                feature=featuring,
                                genre=genre,
                                tags=tags,
                                description=description,
                                artwork=artwork_upload_result['url'],
                                source=audio_upload_result['url'],
                                artwork_public_id=artwork_upload_result['public_id'],
                                audio_public_id=audio_upload_result['public_id'])
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Upload Failed!', 'error')
                    return redirect(url_for('main.home'))
                

@song.route('/song/edit/<int:song_id>', methods=('GET', 'POST'))
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
                if artwork_file and audio_file and allowed_file(artwork_file.filename) and allowed_file(audio_file.filename):
                    unique_artwork_filename = make_unique(artwork_file.filename)
                    unique_audio_filename = make_unique(audio_file.filename)
                    artwork_file.filename = secure_filename(unique_artwork_filename)
                    audio_file.filename = secure_filename(unique_audio_filename)
                    artwork_upload_result = cloudinary.uploader.upload(artwork_file, public_id=unique_artwork_filename)
                    audio_upload_result = cloudinary.uploader.upload_large(audio_file, public_id=unique_audio_filename, resource_type="video")
                    Song.update(artist=artist,
                                title=title,
                                feature=featuring,
                                genre=genre,
                                tags=tags,
                                description=description,
                                artwork=artwork_upload_result['url'],
                                source=audio_upload_result['url'],
                                artwork_public_id=artwork_upload_result['public_id'],
                                source_public_id=audio_upload_result['public_id']).where(Song.id == song_id).execute()
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Upload Failed!', 'error')
                    return redirect(url_for('main.home'))
                    

@song.route('/song/delete/<int:song_id>', methods=('GET', 'POST'))
def delete_song(song_id):
    cloudinary.uploader.destroy(Song.get(Song.id == song_id).artwork_public_id)
    cloudinary.uploader.destroy(Song.get(Song.id == song_id).source_public_id, resource_type="video")
    Song.delete().where(Song.id == song_id).execute()
    flash('Song deleted!', 'success')
    return redirect(url_for('main.home'))


@song.route('/song/<int:song_id>', methods=['GET', 'POST'])
def view_song(song_id):
    year = datetime.date.today().year
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
    return render_template('song/song.html', songs=songs, comments=comments, year=year)


@song.route('/favorite/<int:song_id>', methods=['GET', 'POST'])
@login_required
def favorite(song_id):
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
    return render_template('/partials/song-reactions.html', song=song)


@song.route('/unfavorite/<int:song_id>', methods=['GET', 'POST'])
@login_required
def unfavorite(song_id):
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
    return render_template('/partials/song-reactions.html', song=song)


@song.route('/stream/<int:song_id>', methods=['GET', 'POST'])
@login_required
def stream(song_id):
    songs = Song.select().where(Song.id == song_id)
    song = songs[0]
    numberOfStreams = song.numStreams
    
    Song.update(
        numStreams=numberOfStreams + 1
    ).where(
        Song.id == song.id
    ).execute()
    return redirect(request.referrer)