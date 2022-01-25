from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from peewee import *
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
bootstrap =  Bootstrap()


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.TestConfig')
    
    db.init_app(app)    
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        from app.templates.auth.auth import auth 
        from app.templates.profile.profile import profile
        from app.templates.feed.feed import feed
        from app.templates.feed.song import song
        from app.templates.feed.post import post
        
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(feed)
        app.register_blueprint(song)
        app.register_blueprint(post)
            
        from app.views import views
        app.register_blueprint(views)
        
        db.create_all()

        return app
