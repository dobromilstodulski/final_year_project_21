import os
import os.path
import librosa
import requests
import wave
import io
from urllib.request import urlopen
import pydub
from flask import Blueprint, jsonify
from app.models import Song
from app.templates.audio.music_note_detection import note_detect


api = Blueprint('api', __name__, url_prefix='/api')

pydub.AudioSegment.converter = r"C:\\Users\\bb100\\Documents\\Programs\\ffmpeg-2022-05-02-git-40f2ea971f-essentials_build\\ffmpeg-2022-05-02-git-40f2ea971f-essentials_build\\bin\\ffmpeg.exe"
pydub.AudioSegment.ffprobe = r"C:\\Users\\bb100\\Documents\\Programs\\ffmpeg-2022-05-02-git-40f2ea971f-essentials_build\\ffmpeg-2022-05-02-git-40f2ea971f-essentials_build\\bin\\ffprobe.exe"

@api.route('/song/tempo/<int:song_id>', methods=['GET'])
def tempo(song_id):
    audio = Song.get(Song.id == song_id).source
    
    wav = io.BytesIO()

    with urlopen(audio) as r:
        r.seek = lambda *args: None  # allow pydub to call seek(0)
        pydub.AudioSegment.from_file(r).export(wav, "wav")

    wav.seek(0)
    
    y, sr = librosa.load(wav)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    return jsonify(tempo = '{:.2f}'.format(tempo))


@api.route('/song/key/<int:song_id>', methods=['GET'])
def key(song_id):
    audio = Song.get(Song.id == song_id).source
    wav = io.BytesIO()

    with urlopen(audio) as r:
        r.seek = lambda *args: None  # allow pydub to call seek(0)
        pydub.AudioSegment.from_file(r).export(wav, "wav")

    wav.seek(0)
    
    audio_file = wave.open(wav)
    key = note_detect(audio_file)
    return jsonify(key = str(key))
