from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, database
import app.models
from app import login_manager, db, bcrypt
#from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
	try:
		return User.get(User.id == id)
	except app.models.DoesNotExist:
		return None

@auth.before_request
def before_request():
    """Connect to database before each request
            g is a global object, passed around all time in flask, used to setup things which
            we wanna have available everywhere.
    """
    g.db = database
    g.db.connect()
    g.user = current_user


@auth.after_request
def after_request(response):
    """close all database connection after each request"""
    g.db.close()
    return response

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # code to validate and add user to database goes here
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')

        if username == '' or fullname == '' or email == '' or password == '' or gender == '' or birthday == '':
            flash('Please fill out all the values!', 'warning')
            
        elif User.select().where(User.email == email):
            flash('Email already in use!', 'danger')
            return redirect(url_for('auth.register'))
        
        elif User.select().where(User.username == username):
            flash('Username already in use!', 'danger')
            return redirect(url_for('auth.register'))
        
        else:
            User.create_user(
                username=username,
                fullname=fullname,
                email=email,
                password=password,
                gender=gender,
                birthday=birthday,
                description=''
            )
            flash('Successfully Registered!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

'''
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # code to validate and add user to database goes here
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')

        if username == '' or fullname == '' or email == '' or password == '' or gender == '' or birthday == '':
            flash('Please fill out all the values!', 'warning')

        else:
            user = User.query.filter_by(email=email).first()

            if user:  # if a user is found, we want to redirect back to signup page so user can try again
                flash('Email address or username already exists!', 'error')
                return redirect(url_for('auth.register'))

            new_user = User(username=username, fullname=fullname, email=email, password=generate_password_hash(password),
                            gender=gender, birthday=birthday, profile_picture='/static/images/default_profile_picture.png',
                            description=None)

            db.session.add(new_user)
            db.session.commit()

            flash('Successfully Registered!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
'''


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == '' or password == '':
            flash('Please fill out all the values!', 'warning')
            
        else:
            try:
                user = User.get(User.email == email)
            except app.models.DoesNotExist:
                flash('Your email does not match!', 'error')
            if check_password_hash(user.password, password):
                login_user(user)
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('profile.welcome'))
            else:
                flash('Your password does not match!', 'error')
    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('views.index'))

@auth.route('/test')
def test():
    return render_template('auth/test.html', form=LoginForm())

