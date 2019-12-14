from flask_login import login_required
from flask import render_template
from flask import url_for
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    return render_template('index.html',
                           title='Home',
                           username='New user'
)