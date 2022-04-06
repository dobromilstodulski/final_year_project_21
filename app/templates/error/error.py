from flask import Blueprint, g, render_template, redirect, url_for, request, flash, abort, jsonify
from app import app

@app.errorhandler('404')
def page_not_found(e):
    return render_template('/error/404.html'), 404#