from flask import Blueprint, redirect
from flask_login import login_required
from app.models import Song

audio = Blueprint('audio', __name__)

@audio.route('/play/<int:song_id>')
@login_required
def returnAudioFile(song_id):
    song = Song.get(Song.id == song_id)
    path_to_audio_file = redirect("https://fypkmpsr.s3.eu-west-1.amazonaws.com/" + song.source)
    return path_to_audio_file