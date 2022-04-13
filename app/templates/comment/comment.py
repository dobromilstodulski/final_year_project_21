from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, database, Comment, Like

comment = Blueprint('comment', __name__)

@comment.route('/comment/edit/<int:comment_id>', methods=('GET', 'POST'))
def edit_comment(comment_id):
    if request.method == 'POST':
        content = request.form.get('content')
        if content == '':
            flash('Please fill out all the values!', 'warning')
        else:
            Post.update(content=content,
                        isEdited = 1
                        ).where(Comment.id == comment_id).execute()
            flash("Comment Updated!", "success")
            return redirect(request.referrer)


@comment.route('/comment/delete/<int:comment_id>', methods=('GET', 'POST'))
def delete_comment(comment_id):
    if request.method == 'POST':
        Post.delete().where(Comment.id == comment_id).execute()
        flash("Comment Deleted!", "success")
        return redirect(request.referrer)