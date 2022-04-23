import os
from dotenv import load_dotenv
from flask import Flask, render_template
from peewee import *
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_moment import Moment
from acrcloud.recognizer import ACRCloudRecognizer, ACRCloudRecognizeType

load_dotenv()

login_manager = LoginManager()
socketio = SocketIO()
moment = Moment()

config = {
    'host': os.getenv("HOST"),
    'access_key': os.getenv("ACCESS_KEY"),
    'access_secret': os.getenv("ACCESS_SECRET"),
    'recognize_type': ACRCloudRecognizeType.ACR_OPT_REC_AUDIO, # you can replace it with [ACR_OPT_REC_AUDIO,ACR_OPT_REC_HUMMING,ACR_OPT_REC_BOTH], The     SDK decide which type fingerprint to create accordings to "recognize_type".
    'debug':False,
    'timeout': 10
}

re = ACRCloudRecognizer(config)

def bad_request(e):
    return render_template('/error/400.html'), 400

def unauthorized(e):
    return render_template('/error/401.html'), 401

def forbidden(e):
    return render_template('/error/403.html'), 403

def page_not_found(e):
    return render_template('/error/404.html'), 404

def internal_server_error(e):
    return render_template('/error/500.html'), 500

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.TestConfig')

    db.init_app(app)
    socketio.init_app(app)
    moment.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app.templates.auth.auth import auth
        from app.templates.profile.profile import profile
        from app.templates.song.song import song
        from app.templates.post.post import post
        from app.templates.chat.chat import chat
        from app.templates.audio.audio import audio
        from app.templates.legal.legal import legal
        from app.templates.search.search import search
        from app.templates.comment.comment import comment
        from app.templates.main.main import main
        from app.api.api import api

        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(song)
        app.register_blueprint(post)
        app.register_blueprint(chat)
        app.register_blueprint(audio)
        app.register_blueprint(legal)
        app.register_blueprint(search)
        app.register_blueprint(comment)
        app.register_blueprint(main)
        app.register_blueprint(api)

        from app.views import views
        app.register_blueprint(views)
        
        app.register_error_handler(400, bad_request)
        app.register_error_handler(401, unauthorized)
        app.register_error_handler(403, forbidden)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(404, internal_server_error)

        return app