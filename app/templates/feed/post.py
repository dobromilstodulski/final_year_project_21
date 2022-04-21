from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, jsonify, make_response
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
import time
import random
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.flask_utils import object_list

post = Blueprint('post', __name__)


@post.route('/post/feed')
def post_feed():
    posts = current_user.get_post_feed()
    return render_template('feed/post_feed.html', stream=posts, user=User, format=format)


@post.route('/post/new', methods=('GET', 'POST'))
def new_post():
    if request.method == 'POST':
        content = request.form.get('content')
        file = request.files["media"]
        if not file:
            if content == '':
                flash('Please fill out all the values!', 'warning')
            else:
                Post.create(user_id=current_user.id,
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
                    Post.create(user_id=current_user.id,
                                content=content,
                                media=file.filename,
                                isMedia=1)
                    flash('Upload Succeeded!', 'success')
                    return redirect(url_for('post.post_feed'))
                else:
                    return redirect(url_for('post.post_feed'))
                

'''
@post.route('/edit_post/<int:post_id>', methods=('GET', 'POST'))
def edit_post(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        file = request.files["media"]
        if content == '':
            flash('Please fill out all the values!', 'warning')
        else:
            Post.update(content=content).where(Post.id == post_id).execute()
            flash("Post Updated!", "success")
            return redirect(request.referrer)
        if file and allowed_file(file.filename):
                if file.filename == "" and content == '':
                    flash('Please fill out all the values!', 'warning')
                else:
                    unique_filename = make_unique(file.filename)
                    file.filename = secure_filename(unique_filename)
                    upload_file(file)
                    Post.update(content=content,
                                media=file.filename,
                                isMedia=1).where(Post.id == post_id).execute()
                    flash('Upload Succeeded!', 'success')
                    return redirect(request.referrer)
'''


@post.route('/post/edit/<int:post_id>', methods=('GET', 'POST'))
def edit_post_media_null(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        if content == '':
            flash('Please fill out all the values!', 'warning')
        else:
            Post.update(content=content).where(Post.id == post_id).execute()
            flash("Post Updated!", "success")
            return redirect(request.referrer)


@post.route('/post/edit/media/<int:post_id>', methods=('GET', 'POST'))
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


@post.route('/post/delete/<int:post_id>', methods=('GET', 'POST'))
def delete_post_media_null(post_id):
    if request.method == 'POST':
        Post.delete().where(Post.id == post_id).execute()
        flash("Post Deleted!", "success")
        return redirect(request.referrer)


@post.route('/post/delete/media/<int:post_id>', methods=('GET', 'POST'))
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
    return render_template('feed/post.html', posts=posts, format=format, comments=comments)


@post.route('/like/<int:post_id>', methods=['GET', 'POST'])
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
    return render_template('/partials/post-reactions.html', post=post)


@post.route('/unlike/<int:post_id>', methods=['GET', 'POST'])
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
    return render_template('/partials/post-reactions.html', post=post)

###### User ######


@post.route('/my_post_feed')
def my_post_feed():
    posts = current_user.get_private_post_feed()
    return render_template('feed/post_feed.html', stream=posts, user=User, format=format)

@post.route('/posts')
def posts_posts():
    return render_template('feed/posts.html', posts=Post)

'''
heading = "Lorem ipsum dolor sit amet."

content = """
Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
Repellat inventore assumenda laboriosam, 
obcaecati saepe pariatur atque est? Quam, molestias nisi.
"""

db = list()  # The mock database

articles = 500  # num posts to generate

quantity = 20  # num posts to return per request

for x in range(articles):

    """
    Creates messages/posts by shuffling the heading & content 
    to create random strings & appends to the db
    """

    heading_parts = heading.split(" ")
    random.shuffle(heading_parts)

    content_parts = content.split(" ")
    random.shuffle(content_parts)

    db.append([x, " ".join(heading_parts), " ".join(content_parts)])
    
@post.route("/load")
def load():
    """ Route to return the posts """

    time.sleep(0.2)  # Used to simulate delay

    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(db[0: quantity]), 200)

        elif counter == articles:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res

@post.route("/posts2")
def posts2_posts2():
    return render_template('feed/post2.html')
'''

@post.route('/posts3')
def posts3_posts3():
    all_items = (Post.select())                                               
    return object_list("feed/post3.html", paginate_by=10, query=all_items) 

'''
@post.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    posts = Post.select().where(Post.id == post_id)
    if posts.count() == 0:
       abort(404)
    return render_template('feed/post_feed.html', stream=posts, format=format)
'''
