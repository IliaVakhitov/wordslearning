from flask import render_template
from wlapp.auth import bp
from wlapp.auth.forms import LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', title='Sign In', form=form)

