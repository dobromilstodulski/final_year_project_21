from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, database
from app import login_manager

profile = Blueprint('profile', __name__)


@profile.before_request
def before_request():
    """Connect to database before each request
            g is a global object, passed around all time in flask, used to setup things which
            we wanna have available everywhere.
    """
    g.db = database
    g.db.connect()
    g.user = current_user


@profile.after_request
def after_request(response):
    """close all database connection after each request"""
    g.db.close()
    return response


@profile.route('/my')
def myprofile():
    return 'profile goes here'


@profile.route('/welcome')
@login_required
def welcome():
    user = current_user
    return render_template('profile/welcome.html', user=user)