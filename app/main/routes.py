from flask_login import login_required
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from app.models import Dictionary
from app.models import Word
from app.main import bp
from app.main.forms import EditDictionaryForm
from app.main.forms import EditWordForm
from app import db


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    return render_template('index.html',
                           title='Home',
                           username='Guest'
)


@bp.route('/dictionaries', methods=['GET', 'POST'])
#@login_required
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


@bp.route('/dictionary/<int:dictionary_id>', methods=['GET', 'POST'])
#@login_required
def dictionary(dictionary_id):
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

    return render_template('main/dictionary.html',
                           title=dictionary.dictionary_name,
                           dictionary=dictionary,
                           form=dictionary_form)


@bp.route('/word/<int:word_id>', methods=['GET', 'POST'])
#@login_required
def word(word_id):
    word = Word.query.filter_by(id=word_id).first_or_404()
    word_form = EditWordForm(word.spelling, word.definition)

    if word_form.validate_on_submit():
        new_spelling = word_form.spelling.data
        new_definition = word_form.definition.data
        word.spelling = new_spelling
        word.definition = new_definition
        db.session.commit()
        flash('Word saved!')
        return redirect(url_for('main.word', word_id=word.id))

    elif request.method == 'GET':
        word_form.spelling.data = word.spelling
        word_form.definition.data = word.definition

    return render_template('main/word.html',
                           title=word.spelling,
                           word=word,
                           form=word_form)


@bp.route('/addword/<int:dictionary_id>', methods=['GET', 'POST'])
#@login_required
def addword(dictionary_id):
    dictionary = Dictionary.query.filter_by(id=dictionary_id).first_or_404()
    word_form = EditWordForm("", "")
    if word_form.validate_on_submit():
        word_spelling = word_form.spelling.data
        word_definition = word_form.definition.data
        word = Word(dictionary_id=dictionary.id, spelling=word_spelling, definition=word_definition)
        db.session.add(word)
        db.session.commit()
        flash('Dictionary saved!')
        return redirect(url_for('main.dictionary', dictionary_id=dictionary.id))

    return render_template('main/addword.html',
                           title='Add word',
                           dictionary=dictionary,
                           form=word_form)


