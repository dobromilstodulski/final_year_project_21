import datetime
from flask import Blueprint, render_template

legal = Blueprint('legal', __name__)

@legal.route('/cookies-policy')
def cookies_policy():
    year = datetime.date.today().year
    return render_template('legal/cookies-policy.html', year=year)

@legal.route('/privacy-policy')
def privacy_policy():
    year = datetime.date.today().year
    return render_template('legal/privacy-policy.html', year=year)

@legal.route('/terms-and-conditions')
def terms_of_service():
    year = datetime.date.today().year
    return render_template('legal/terms-and-conditions.html', year=year)