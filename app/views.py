from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

views = Blueprint('views', __name__)

'''
@views.before_request
def before_request():
    """Connect to database before each request
            g is a global object, passed around all time in flask, used to setup things which
            we wanna have available everywhere.
    """
    g.db = database
    g.db.connect()
    g.user = current_user


@views.after_request
def after_request(response):
    """close all database connection after each request"""
    g.db.close()
    return response
'''


@views.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

'''
@views.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # code to validate and add user to database goes here
        username = request.form.get('registerUsername')
        name = request.form.get('registerFullname')
        email = request.form.get('registerEmail')
        password = request.form.get('registerPassword')
        gender = request.form.get('registerGender')
        birthday = request.form.get('registerBirthday')

        if username == None or name == None or email == None or password == None or gender == None or birthday == None:
            flash('Please fill out all the values!')

        else:
            user = User.query.filter_by(email=email).first()

            if user:  # if a user is found, we want to redirect back to signup page so user can try again
                flash('Email address or username already exists!')
                return redirect(url_for('index'))

            else:
                User.create_user(
                    username=username,
                    name=name,
                    email=email,
                    password=password,
                    gender=gender,
                    birthday=birthday
                )
                return redirect(url_for('feed'))
'''