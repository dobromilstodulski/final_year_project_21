from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, send_file, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, database, Comment, Like, Song
import os
from app import re
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType

audio = Blueprint('audio', __name__)

@audio.route('/play/<int:song_id>')
def returnAudioFile(song_id):
    song = Song.get(Song.id == song_id)
    path_to_audio_file = redirect("https://fypkmpsr.s3.eu-west-1.amazonaws.com/" + song.source)
    return path_to_audio_file
    
@audio.route('/check', methods=['GET', 'POST'])
def check_copyright():
    uploaded_file = request.files['file']
    if uploaded_file != '':
        uploaded_file.save(uploaded_file.filename)

    #buf = open('C:/Users/bb100/Documents/Final Year Project/final_year_project_21/shakeit.wav', 'rb').read()    
    results = eval(re.recognize_by_file(uploaded_file.filename, 0))
    #results = eval(re.recognize_by_filebuffer(buf, 0))
    #results = check_file(uploaded_file.filename)
    return results
    
@audio.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('/audio/audio.html')