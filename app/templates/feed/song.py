from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, database
import app.models
from app import login_manager

song = Blueprint('song', __name__)

@login_manager.user_loader
def load_user(id):
	try:
		return User.get(User.id == id)
	except app.models.DoesNotExist:
		return None

@song.before_request
def before_request():
    """Connect to database before each request
            g is a global object, passed around all time in flask, used to setup things which
            we wanna have available everywhere.
    """
    g.db = database
    g.db.connect()
    g.user = current_user


@song.route('/song_feed')
def song_feed():
    return render_template('feed/song_feed.html')

@song.route('/new_song', methods=('GET', 'POST'))
@login_required
def post():
    if request.method == 'POST':
        content = request.form.get('content')
        media = request.form.get('media')
        
        if content == '':
            flash('Please fill out all the values!', 'warning')
            
        else:
            if media:  # Media is present
                Post.create(user=g.user._get_current_object(),
                               content=content,
                               media=media,
                               ismedia=1)
            else:  # No image uploaded
                Post.create(user=g.user._get_current_object(),
                               content=content)
        flash("Post Created!", "success")
        return redirect(url_for('post_feed'))
    return render_template('feed/post_feed.html')