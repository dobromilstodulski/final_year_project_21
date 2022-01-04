from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, Length
from app.models import User

def username_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('User with this username already exists.')

def email_exists(form,field):
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('User with this email already exists.')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$', message = ("Username should be one word, letters, numbers and underscores only.")), username_exists])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3), EqualTo('password2', message = 'Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), email_exists])
    gender = SelectField('Gender', choices=[('M','Male'), ('F','Female'), ('O', 'Other'), ('N/A','Rather Not Say')])
    birthday = DateField('Birthday',  format='%d-%m-%Y')
    submit = SubmitField("Register")
    
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has already been registered!')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")