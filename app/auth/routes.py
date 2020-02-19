from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from sqlalchemy import func
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Dictionary, Word, LearningIndex
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
    dictionaries = Dictionary.query.filter_by(user_id=current_user.id).all()
    dict_ids = [d.id for d in dictionaries]
    words = Word.query.filter(Word.dictionary_id.in_(dict_ids)).all()
    total_words = len(words)
    words_ids = [w.id for w in words]
    words_learned = LearningIndex.query.filter(LearningIndex.word_id.in_(words_ids)).filter_by(index=100).count()
    total_dictionaries = len(dictionaries)
    # TODO get progress as a sum from all words, then divide on number of words
    # sub_query = db.session.query(func.sum(LearningIndex.index).label("index_progress"))
    # index_progress = sub_query.group_by().all().index_progress
    # not sql solution
    learning_index_list = LearningIndex.query.filter(LearningIndex.word_id.in_(words_ids)).all()
    index_progress = 0
    for li_entry in learning_index_list:
        index_progress += li_entry.index
    progress = round(index_progress / total_words, 2)
    return render_template('auth/user.html',
                           user=user,
                           total_dictionaries=total_dictionaries,
                           total_words=total_words,
                           words_learned=words_learned,
                           progress=progress)
