import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app.models import User, Relationship
import app.models
from app.utils import allowed_file, make_unique, upload_file
from werkzeug.utils import secure_filename

profile = Blueprint('profile', __name__)


@profile.route('/profile/<username>')
@login_required
def userProfile(username):
    year = datetime.date.today().year
    user = User.get(User.username ** username)
    posts = User.get_posts(user)
    following_count = User.select().join(Relationship, on=Relationship.to_user).where(
        Relationship.from_user == user).count()
    followers_count = User.select().join(Relationship, on=Relationship.from_user).where(
        Relationship.to_user == user).count()
    songs = User.get_songs(user)
    song_count = User.get_songs(user).count()
    comments = User.get_comments(user)
    return render_template('profile/profile.html', user=user, following_count=following_count, followers_count=followers_count, posts=posts, songs=songs, song_count=song_count, comments=comments, year=year)


@profile.route('/edit-user-details', methods=['GET', 'POST'])
@login_required
def editUserDetails():
    user = current_user
    file = request.files["profilePicture"]
    username = request.form.get('username')
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    gender = request.form.get('gender')
    birthday = request.form.get('birthday')
    description = request.form.get('description')
    if file.filename == "" and username == '' and fullname == '' and email == '' and gender == '' and birthday == '':
        flash('Please fill out all the values!', 'warning')
    else:
        if file and allowed_file(file.filename):
            unique_filename = make_unique(file.filename)
            file.filename = secure_filename(unique_filename)
            upload_file(file)
    User.update(
            username = username,
            fullname = fullname,
            email = email,
            gender = gender,
            birthday = birthday,
            profilePicture = file.filename,
            description = description
        ).where(
            User.username == user.username
        ).execute()
    return redirect(url_for('profile.userProfile', username=user.username))


@profile.route('/following')
@login_required
def following():
    year = datetime.date.today().year
    user = current_user
    following = User.following(user)
    following_count = User.select().join(Relationship, on=Relationship.to_user).where(
        Relationship.from_user == user).count()
    followers_count = User.select().join(Relationship, on=Relationship.from_user).where(
        Relationship.to_user == user).count()
    return render_template('profile/following.html', user=user, following=following, following_count=following_count, followers_count=followers_count, year=year)


@profile.route('/followers')
@login_required
def followers():
    year = datetime.date.today().year
    user = current_user
    followers = User.followers(user)
    following_count = User.select().join(Relationship, on=Relationship.to_user).where(
        Relationship.from_user == user).count()
    followers_count = User.select().join(Relationship, on=Relationship.from_user).where(
        Relationship.to_user == user).count()
    return render_template('profile/followers.html', user=user, followers=followers, following_count=following_count, followers_count=followers_count, year=year)


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
                from_user=current_user,
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
                from_user=current_user,
                to_user=to_user
            ).delete_instance()
        except app.models.IntegrityError:
            pass
        else:
            flash("You've unfollowed @{}!".format(to_user.username), "success")
    return redirect(request.referrer)