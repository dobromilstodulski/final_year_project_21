from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort

legal = Blueprint('legal', __name__)

@legal.route('/cookies-policy')
def cookies_policy():
    return render_template('legal/cookies-policy.html')

@legal.route('/privacy-policy')
def privacy_policy():
    return render_template('legal/privacy-policy.html')

@legal.route('/terms-and-conditions')
def terms_of_service():
    return render_template('legal/terms-and-conditions.html')