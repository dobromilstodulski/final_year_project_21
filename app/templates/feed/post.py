from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, database, Comment, Like
import app.models
from app import login_manager
from timeago import format
from app.utils import allowed_file, make_unique, upload_file, upload_file_to_s3, upload_object, upload_file2, upload_file_object, send_to_s3
from werkzeug.utils import secure_filename
from urllib.parse import urljoin
import os
import boto3

post = Blueprint('post', __name__)


@login_manager.user_loader
def load_user(id):
    try:
        return User.get(User.id == id)
    except app.models.DoesNotExist:
        return None


@post.before_request
def before_request():
    """Connect to database before each request
            g is a global object, passed around all time in flask, used to setup things which
            we wanna have available everywhere.
    """
    g.db = database
    g.db.connect()
    g.user = current_user


@post.after_request
def after_request(response):
    """close all database connection after each request"""
    g.db.close()
    return response


@post.route('/post_feed')
def post_feed():
    posts = current_user.get_post_feed()
    return render_template('feed/post_feed.html', stream=posts, user=User, format=format)


@post.route('/new_post', methods=('GET', 'POST'))
@login_required
def new_post():
    if request.method == 'POST':
        content = request.form.get('content')
        media = request.files.get('media')
           
        if media and allowed_file(media.filename):  # Image/Video is present and file extension is allowed
            if content == '' and media.filename == '':
                flash('Please fill out all the values!', 'warning') 
            else:
                unique_filename = make_unique(media.filename)
                #filename = secure_filename(unique_filename.filename)
                output = upload_file_to_s3(media)
                if output:
                    Post.create(user=g.user._get_current_object(),
                                content=content,
                                image=urljoin(os.getenv("AWS_BUCKET_URL"), media),
                                ismedia=1)
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('post.post_feed'))
                else:
                    flash('Upload Failed!', 'error')
                    return redirect(url_for('post.post_feed'))
        else:  # No Image/Video uploaded
            if content == '':
                flash('Please fill out all the values!', 'warning')
            else:
                Post.create(user=g.user._get_current_object(),
                            content=content)
        flash("Post Created!", "success")
        return redirect(url_for('post.post_feed'))
    return render_template('feed/post_feed.html')


@post.route('/new_post2', methods=('GET', 'POST'))
@login_required
def new_post2():
    if request.method == 'POST':
        content = request.form.get('content')
        media = request.files['media']

        #unique_filename = make_unique(media)
        #filename = secure_filename(unique_filename.filename)
        filename = secure_filename(media.filename)
        destination = media.save(urljoin(os.getenv("AWS_BUCKET_URL"), filename))
        upload_file(media)
        Post.create(user=g.user._get_current_object(),
                    content=content,
                    image=destination,
                    ismedia=1)
        flash('Upload Succeeded!', 'success')
        return redirect(url_for('post.post_feed'))
    return render_template('feed/post_feed.html')

@post.route('/new_post4', methods=('GET', 'POST'))
def upload_file2():
    if request.method == 'POST':
        content = request.form.get('content')
        if "media" not in request.files:
            if content == '':
                flash('Please fill out all the values!', 'warning')
            else:
                Post.create(user=g.user._get_current_object(),
                            content=content)
                flash("Post Created!", "success")
                return redirect(url_for('post.post_feed'))
        file = request.files["media"]
        if "media" in request.files:
            if file.filename == "" and content == '':
                flash('Please fill out all the values!', 'warning')
            else: 
                if file and allowed_file(file.filename):
                    unique_filename = make_unique(file.filename)
                    file.filename = secure_filename(unique_filename)
                    send_to_s3(file, os.getenv("AWS_BUCKET_NAME"))
                    Post.create(user=g.user._get_current_object(),
                                content=content,
                                media=file.filename,
                                isMedia=1)
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('post.post_feed'))
                else:
                    return redirect("/")
	

@post.route('/new_post3', methods=('GET', 'POST'))
def upload_file():
    if "media" not in request.files:
        return "No user_file key in request.files"
    file = request.files["media"]
    if file.filename == "":
        return "Please select a file"
    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, os.getenv("AWS_BUCKET_NAME"))
        return str(output)
    else:
        return redirect("/")	


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
                user_id=g.user._get_current_object(),
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
        user_id=g.user._get_current_object(),
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
        user_id=g.user._get_current_object(),
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

