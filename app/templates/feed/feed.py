from flask import Blueprint, render_template
from app.models import User
from app import login_manager

feed = Blueprint('feed', __name__)

@feed.route('/feed')
def post_feed():
    return render_template('feed/feed.html')