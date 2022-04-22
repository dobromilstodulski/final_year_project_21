import os
import os.path
from statistics import correlation
import librosa
import requests
import json
import wave
from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, jsonify, make_response
from app.models import User, Song, Comment, Favorite
from app.templates.audio.keyfinder import Tonal_Fragment
from app.templates.audio.music_note_detection import note_detect


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/song/tempo/<int:song_id>', methods=['GET'])
def tempo(song_id):
    song = Song.get(Song.id == song_id)
    if not os.path.isfile(os.path.join('app/static/uploads', song.source)):
        URL = "https://fypkmpsr.s3.eu-west-1.amazonaws.com/" + song.source
        response = requests.get(URL)
        with open(os.path.join('app/static/uploads', song.source), "wb") as f:
            f.write(response.content)
    else:
        y, sr = librosa.load(os.path.join('app/static/uploads', song.source))
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        return jsonify(tempo = '{:.2f}'.format(tempo))


@api.route('/song/key/<int:song_id>', methods=['GET'])
def key(song_id):
    song = Song.get(Song.id == song_id)
    if not os.path.isfile(os.path.join('app/static/uploads', song.source)):
        URL = "https://fypkmpsr.s3.eu-west-1.amazonaws.com/" + song.source
        response = requests.get(URL)
        with open(os.path.join('app/static/uploads', song.source), "wb") as f:
            f.write(response.content)
    else:
        filename = os.path.join('app/static/uploads', song.source)
        audio_file = wave.open(filename)
        key = note_detect(audio_file)
        return jsonify(key = str(key))
