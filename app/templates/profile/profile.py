from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Relationship, Post, database, Comment, Like
import app.models
from app import login_manager
from timeago import format

profile = Blueprint('profile', __name__)


@profile.route('/my')
def myprofile():
    user = current_user
    posts = User.get_posts(user)
    following_count = User.select().join(Relationship, on=Relationship.to_user).where(
        Relationship.from_user == user).count()
    followers_count = User.select().join(Relationship, on=Relationship.from_user).where(
        Relationship.to_user == user).count()
    songs = User.get_songs(user)
    song_count = User.get_songs(user).count()
    return render_template('profile/profile.html', user=user, following_count=following_count, followers_count=followers_count, posts=posts, songs=songs, song_count=song_count)


@profile.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = User.get(User.username ** username)
    except app.models.DoesNotExist:
        abort(404)
    else:
        try:
            Relationship.create(
                from_user=g.user._get_current_object(),
                to_user=to_user
            )
        except app.models.IntegrityError:
            pass
        else:
            flash("You're now following @{}!".format(to_user.username), "success")
    return redirect(request.referrer)


@profile.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = User.get(User.username ** username)
    except app.models.DoesNotExist:
        abort(404)
    else:
        try:
            Relationship.get(
                from_user=g.user._get_current_object(),
                to_user=to_user
            ).delete_instance()
        except app.models.IntegrityError:
            pass
        else:
            flash("You've unfollowed @{}!".format(to_user.username), "success")
    return redirect(request.referrer)


@profile.route('/welcome')
@login_required
def welcome():
    user = current_user
    return render_template('profile/welcome.html', user=user)
