import pusher
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from peewee import *
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_moment import Moment

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
socketio = SocketIO()
moment = Moment()

pusher_client = pusher.Pusher(
    app_id='1363194',
    key='6eb53b420f4f837b63e2',
    secret='1a50a60455b3c70fea61',
    cluster='eu',
    ssl=True
)


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.TestConfig')

    db.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
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

        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(feed)
        app.register_blueprint(song)
        app.register_blueprint(post)
        app.register_blueprint(chatroom)

        from app.views import views
        app.register_blueprint(views)

        db.create_all()

        return app
