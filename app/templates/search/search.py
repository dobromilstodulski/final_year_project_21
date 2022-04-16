from flask import Blueprint, g, jsonify, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Song
import app.models
from app import login_manager
from timeago import format
from flask_paginate import Pagination, get_page_parameter

search = Blueprint('search', __name__)

@search.route('/search', methods=['GET', 'POST'])
def search_query():
    #query = request.args['search']
    #query = request.GET.get('search') 
    #query = request.form.get('search')
    user = User
    query = request.args.get('search')
    #posts_result = Post.select().where(Post.content.contains(query))
    users_result = User.select().where(User.fullname.contains(query) | User.username.contains(query))
    posts_result = Post.select().where(Post.content.contains(query))
    songs_result = Song.select().where(Song.title.contains(query) | Song.artist.contains(query) | Song.feature.contains(query))
    return render_template('search/search.html', query=query, users_result=users_result, posts_result=posts_result, songs_result=songs_result, user=user)
    