from flask_login import login_required
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import jsonify
from app.models import Dictionary
from app.models import Word
from app.main import bp
from app.main.forms import EditDictionaryForm
from app.main.forms import EditWordForm
from app import db


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html',
                           title='Home',
                           username='Guest'
)


@bp.route('/dictionaries', methods=['GET', 'POST'])
# @login_required
def dictionaries():
    dictionary_form = EditDictionaryForm("", "")
    if dictionary_form.validate_on_submit():
        dictionary_name = dictionary_form.dictionary_name.data
        description = dictionary_form.description.data
        dictionary = Dictionary(dictionary_name=dictionary_name, description=description)
        db.session.add(dictionary)
        db.session.commit()
        flash('Dictionary saved!')

    dictionaries = Dictionary.query.order_by('dictionary_name')
    return render_template('main/dictionaries.html',
                           title='Dictionaries',
                           form=dictionary_form,
                           dictionaries=dictionaries)


@bp.route('/dictionary/<int:dictionary_id>')
# @login_required
def dictionary(dictionary_id):
    dictionary = Dictionary.query.filter_by(id=dictionary_id).first_or_404()
    return render_template('main/dictionary.html',
                           title=dictionary.dictionary_name,
                           dictionary=dictionary)


@bp.route('/edit/dictionary/<int:dictionary_id>', methods=['GET', 'POST'])
# @login_required
def edit_dictionary(dictionary_id):
    dictionary = Dictionary.query.filter_by(id=dictionary_id).first_or_404()
    dictionary_form = EditDictionaryForm(dictionary.dictionary_name, dictionary.description)
    if dictionary_form.validate_on_submit():
        new_dictionary_name = dictionary_form.dictionary_name.data
        new_description = dictionary_form.description.data
        dictionary.dictionary_name = new_dictionary_name
        dictionary.description = new_description
        db.session.commit()
        flash('Dictionary saved!')
        return redirect(url_for('main.dictionary', dictionary_id=dictionary.id))

    elif request.method == 'GET':
        dictionary_form.dictionary_name.data = dictionary.dictionary_name

    return render_template('main/edit_dictionary.html',
                           title=dictionary.dictionary_name,
                           dictionary=dictionary,
                           form=dictionary_form)


@bp.route('/word/<int:word_id>')
# @login_required
def word(word_id):
    word = Word.query.filter_by(id=word_id).first_or_404()
    return render_template('main/word.html',
                           title=word.spelling,
                           word=word)


@bp.route('/check_dictionary_name', methods=['POST'])
def check_dictionary_name():
    dictionary_name = request.form['dictionary_name']
    dictionary = Dictionary.query.filter_by(dictionary_name=dictionary_name).first()
    return jsonify({'name_available': dictionary is None})


