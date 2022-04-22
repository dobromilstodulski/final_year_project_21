import os
import os.path
import librosa
import requests
from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, jsonify
from app.models import User, Song, Comment, Favorite


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
    