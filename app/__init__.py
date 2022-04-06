import pusher
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from peewee import *
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_moment import Moment

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
moment = Moment()

pusher_client = pusher.Pusher(
    app_id='1363194',
    key='6eb53b420f4f837b63e2',
    secret='1a50a60455b3c70fea61',
    cluster='eu',
    ssl=True
)

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
        from app.templates.feed.feed import feed
        from app.templates.feed.song import song
        from app.templates.feed.post import post
        from app.templates.chat.chat import chatroom
        from app.templates.audio.audio import audio
        from app.templates.legal.legal import legal

        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(feed)
        app.register_blueprint(song)
        app.register_blueprint(post)
        app.register_blueprint(chatroom)
        app.register_blueprint(audio)
        app.register_blueprint(legal)

        from app.views import views
        app.register_blueprint(views)
        
        app.register_error_handler(400, bad_request)
        app.register_error_handler(401, unauthorized)
        app.register_error_handler(403, forbidden)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(404, internal_server_error)

        db.create_all()

        return app
