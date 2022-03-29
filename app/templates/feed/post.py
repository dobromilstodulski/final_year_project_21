from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, database, Comment, Like
import app.models
from app import login_manager
from timeago import format
from app.utils import allowed_file, make_unique, upload_file, delete_file
from werkzeug.utils import secure_filename
from urllib.parse import urljoin
import os
import boto3

post = Blueprint('post', __name__)


@post.route('/post_feed')
def post_feed():
    posts = current_user.get_post_feed()
    return render_template('feed/post_feed.html', stream=posts, user=User, format=format)


@post.route('/new_post', methods=('GET', 'POST'))
def new_post():
    if request.method == 'POST':
        content = request.form.get('content')
        file = request.files["media"]
        if not file:
            if content == '':
                flash('Please fill out all the values!', 'warning')
            else:
                Post.create(user=g.user._get_current_object(),
                            content=content)
                flash("Post Created!", "success")
                return redirect(url_for('post.post_feed'))
        if file:
            if file.filename == "" and content == '':
                flash('Please fill out all the values!', 'warning')
            else:
                if file and allowed_file(file.filename):
                    unique_filename = make_unique(file.filename)
                    file.filename = secure_filename(unique_filename)
                    upload_file(file)
                    Post.create(user=current_user.id,
                                content=content,
                                media=file.filename,
                                isMedia=1)
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('post.post_feed'))
                else:
                    return redirect("/")


@post.route('/edit_post/media=null/<int:post_id>', methods=('GET', 'POST'))
def edit_post_media_null(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        if content == '':
            flash('Please fill out all the values!', 'warning')
        else:
            Post.update(content=content).where(Post.id == post_id).execute()
            flash("Post Updated!", "success")
            return redirect(request.referrer)


@post.route('/edit_post/media=true/<int:post_id>', methods=('GET', 'POST'))
def edit_post_media_true(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        file = request.files["media"]
        if file.filename == "" and content == '':
            flash('Please fill out all the values!', 'warning')
        else:
            if file and allowed_file(file.filename):
                unique_filename = make_unique(file.filename)
                file.filename = secure_filename(unique_filename)
                upload_file(file)
                Post.update(content=content,
                            media=file.filename,
                            isMedia=1).where(Post.id == post_id).execute()
                flash('Upload Succeeded!', 'success')
                return redirect(request.referrer)
            else:
                return "error"


@post.route('/delete_post/media=null/<int:post_id>', methods=('GET', 'POST'))
def delete_post_media_null(post_id):
    if request.method == 'POST':
        Post.delete().where(Post.id == post_id).execute()
        flash("Post Deleted!", "success")
        return redirect(request.referrer)


@post.route('/delete_post/media=true/<int:post_id>', methods=('GET', 'POST'))
def delete_post_media_true(post_id):
    if request.method == 'POST':
        delete_file(Post.get(Post.id == post_id).media)
        Post.delete().where(Post.id == post_id).execute()
        flash("Post Deleted!", "success")
        return redirect(request.referrer)


@post.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    posts = Post.select().where(Post.id == post_id)
    numberOfComments = posts[0].numComments
    comments = Comment.select().where(Comment.post_id == post_id)
    if request.method == 'POST':
        content = request.form.get('content')

        if content == '':
            flash('Please fill out all the values!', 'warning')

        else:
            Comment.create(
                user_id=current_user.id,
                post_id=post_id,
                comment=content
            )

            Post.update(
                numComments=numberOfComments + 1
            ).where(
                Post.id == post_id
            ).execute()

            flash("Comment Posted!", "success")
            return redirect(request.referrer)

    if posts.count() == 0:
        abort(0)
    return render_template('feed/post.html', stream=posts, format=format, comments=comments)


@post.route('/like/<int:post_id>')
@login_required
def like_post(post_id):
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

    return redirect(request.referrer)


@post.route('/unlike/<int:post_id>')
@login_required
def unlike_post(post_id):
    posts = Post.select().where(Post.id == post_id)
    post = posts[0]
    numberOfLikes = post.numLikes

    Like.get(
        user_id=current_user.id,
        post_id=post
    ).delete_instance()

    Post.update(
        numLikes=numberOfLikes - 1
    ).where(
        Post.id == post.id
    ).execute()
    return redirect(request.referrer)

###### User ######


@post.route('/my_post_feed')
def my_post_feed():
    posts = current_user.get_private_post_feed()
    return render_template('feed/post_feed.html', stream=posts, user=User, format=format)


'''
@post.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    posts = Post.select().where(Post.id == post_id)
    if posts.count() == 0:
       abort(404)
    return render_template('feed/post_feed.html', stream=posts, format=format)
'''
