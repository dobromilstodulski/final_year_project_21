import datetime
from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route("/", methods=['GET', 'POST'])
def index():
    year = datetime.date.today().year
    return render_template('index.html', year=year)