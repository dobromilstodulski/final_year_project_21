import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import User, Post, Song

search = Blueprint('search', __name__)

@search.route('/search', methods=['GET', 'POST'])
@login_required
def search_query():
    year = datetime.date.today().year
    user = User
    query = request.args.get('search')
    users_result = User.select().where(User.fullname.contains(query) | User.username.contains(query))
    posts_result = Post.select().where(Post.content.contains(query))
    songs_result = Song.select().where(Song.title.contains(query) | Song.artist.contains(query) | Song.feature.contains(query))
    return render_template('search/search.html', query=query, users_result=users_result, posts_result=posts_result, songs_result=songs_result, user=user, year=year)
    