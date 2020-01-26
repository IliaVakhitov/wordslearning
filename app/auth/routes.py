from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db_user = User.query.filter_by(username=login_form.username.data).first()
        if db_user is None:
            flash('Invalid username')
            return redirect(url_for('auth.login'))

        if db_user.check_password(login_form.password.data):
            flash('Invalid password')
            return redirect(url_for('auth.login'))
        login_user(db_user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=login_form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        new_user = User(username=registration_form.username.data)
        new_user.secret_question = registration_form.secret_question.data
        new_user.set_password(registration_form.password.data)
        new_user.set_secret_answer(registration_form.secret_answer.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(new_user)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=registration_form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/user.html', user=user)
