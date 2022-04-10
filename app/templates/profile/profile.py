from flask import Blueprint, g, jsonify, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Relationship, Post, database, Comment, Like
import app.models
from app import login_manager
from timeago import format
from flask_paginate import Pagination, get_page_parameter

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
    comments = User.get_comments(user)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=song_count, record_name='songs', per_page=1)
    return render_template('profile/profile.html', user=user, following_count=following_count, followers_count=followers_count, posts=posts, songs=songs, song_count=song_count, comments=comments, pagination=pagination)


@profile.route('/following')
def following():
    user = current_user
    following = User.following(user)
    following_count = User.select().join(Relationship, on=Relationship.to_user).where(
        Relationship.from_user == user).count()
    followers_count = User.select().join(Relationship, on=Relationship.from_user).where(
        Relationship.to_user == user).count()
    return render_template('profile/following.html', user=user, following=following, following_count=following_count, followers_count=followers_count)


@profile.route('/followers')
def followers():
    user = current_user
    followers = User.followers(user)
    following_count = User.select().join(Relationship, on=Relationship.to_user).where(
        Relationship.from_user == user).count()
    followers_count = User.select().join(Relationship, on=Relationship.from_user).where(
        Relationship.to_user == user).count()
    return render_template('profile/following.html', user=user, followers=followers, following_count=following_count, followers_count=followers_count)

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


@profile.route('/welcome')
@login_required
def welcome():
    user = current_user
    return render_template('profile/welcome.html', user=user)

@profile.route('/likepost/<int:post_id>/<action>', methods=['GET', 'POST'])
def like_action(post_id, action):
    posts = Post.select().where(Post.id == post_id)
    post = posts[0]
    numberOfLikes = post.numLikes
    likeunlike = action
    if likeunlike == 'like':
        Like.create(
            user_id=current_user.id,
            post_id=post
        )
        Post.update(
            numLikes=numberOfLikes + 1
        ).where(
            Post.id == post.id
        ).execute()
        return render_template('/feed/like-section.html', post=post)
        #return jsonify({'status': 'success', 'likes': numberOfLikes + 1})
    if likeunlike == 'unlike':
        Like.get(
            user_id=current_user.id,
            post_id=post
        ).delete_instance()
        Post.update(
            numLikes=numberOfLikes - 1
        ).where(
            Post.id == post.id
        ).execute()
        return render_template('/feed/like-section.html', post=post)
        #return jsonify({'status': 'success', 'likes': numberOfLikes - 1})
    
@profile.route('/like2', methods=['GET', 'POST'])
def like_2():
    post_id = request.form['id']
    posts = Post.select().where(Post.id == post_id)
    post = posts[0]
    numberOfLikes = post.numLikes
    Like.create(
        user_id=current_user.id,
        post_id=post
    )
    Post.update(
        numLikes=numberOfLikes + 1
    ).where(
        Post.id == post.id
    ).execute()
    return render_template('/feed/like-section.html', post=post)