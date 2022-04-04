from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, send_file, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, database, Comment, Like, Song

audio = Blueprint('audio', __name__)

@audio.route('/play/<int:song_id>')
def returnAudioFile(song_id):
    song = Song.get(Song.id == song_id)
    path_to_audio_file = redirect("https://fypkmpsr.s3.eu-west-1.amazonaws.com/" + song.source)
    return path_to_audio_file
    
