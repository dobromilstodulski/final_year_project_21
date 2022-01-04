from flask import Blueprint
from app.models import User
from app import login_manager

post = Blueprint('post', __name__)

@post.route('/post_feed')
def post_feed():
    return 'post_feed'