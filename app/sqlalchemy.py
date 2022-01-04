from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    timestamp = db.Column(db.String(120), nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, nullable=False)
    caption = db.Column(db.String(120), nullable=True)
    source = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False, default=datetime.utcnow)
    
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artwork = db.Column(db.String, db.ForeignKey('photo.id'), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    feature = db.Column(db.String(120), nullable=True)
    genre = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(120), nullable=True)
    source = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(120), nullable=False, default=datetime.utcnow)
    
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.String, db.ForeignKey('photo.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False)
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False, default=datetime.utcnow)
    
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False, default=datetime.utcnow)
    
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    attachment = db.Column(db.String(120), nullable=True)
    timestamp = db.Column(db.String(120), nullable=False, default=datetime.utcnow)
    
class Connections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    send_date = db.Column(db.Date)
    approved_date = db.Column(db.Date)
    denied_date = db.Column(db.Date)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _type = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String)
    timestamp = db.Column(db.String(120), nullable=False)