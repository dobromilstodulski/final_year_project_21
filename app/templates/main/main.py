import datetime
from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Comment, Like

main = Blueprint('main', __name__)

@main.route('/index', methods=('GET', 'POST'))
def main_page():
    year = datetime.date.today().year
    posts = current_user.get_post_feed()
    songs = current_user.get_song_feed()
    users = User
    return render_template('main/index.html', posts=posts, songs=songs, users=users, year=year)
