import json
import logging
from flask_login import login_required, current_user
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import jsonify
from sqlalchemy import func

from app.models import Dictionary, CurrentGame
from app.models import Word
from app.main import bp
from app.main.forms import EditDictionaryForm
from app import db
from appmodel.GameGenerator import GameGenerator
from appmodel.GameType import GameType
from appmodel.RevisionGame import RevisionGame


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/dictionaries', methods=['GET', 'POST'])
@login_required
def dictionaries():
    dictionary_form = EditDictionaryForm('', '')
    if dictionary_form.validate_on_submit():
        dictionary_entry = Dictionary(
            dictionary_name=dictionary_form.dictionary_name.data.strip(),
            description=dictionary_form.description.data.strip(),
            user_id=current_user.id)
        db.session.add(dictionary_entry)
        db.session.commit()
        # TODO add logging
        logger.info(f'Dictionary {dictionary_entry.dictionary_name} saved')
        return redirect(url_for('main.edit_dictionary', dictionary_id=dictionary_entry.id))
        # flash('Dictionary saved!')

    dictionaries = Dictionary.query.filter_by(user_id=current_user.id).order_by('dictionary_name')
    return render_template('main/dictionaries.html',
                           title='Dictionaries',
                           form=dictionary_form,
                           dictionaries=dictionaries)


@bp.route('/dictionary/<int:dictionary_id>')
@login_required
def dictionary(dictionary_id):
    dictionary_entry = Dictionary.query.filter_by(id=dictionary_id).first_or_404()
    return render_template('main/dictionary.html',
                           title=dictionary_entry.dictionary_name,
                           dictionary=dictionary_entry)


@bp.route('/edit/dictionary/<int:dictionary_id>', methods=['GET', 'POST'])
@login_required
def edit_dictionary(dictionary_id):
    dictionary_entry = Dictionary.query.filter_by(id=dictionary_id).first_or_404()
    dictionary_form = EditDictionaryForm(dictionary_entry.dictionary_name, dictionary_entry.description)

    if 'delete' in request.form:
        db.session.delete(dictionary_entry)
        db.session.commit()
        return redirect(url_for('main.dictionaries'))

    if dictionary_form.validate_on_submit():
        if 'save_dictionary' in request.form:
            dictionary_entry.dictionary_name = dictionary_form.dictionary_name.data.strip()
            dictionary_entry.description = dictionary_form.description.data.strip()
            # TODO save words list
            db.session.commit()
            flash('Dictionary saved!')
            return redirect(url_for('main.dictionary', dictionary_id=dictionary_entry.id))

        elif 'cancel_edit' in request.form:
            return redirect(url_for('main.dictionary', dictionary_id=dictionary_entry.id))

    if request.method == 'GET':
        dictionary_form.dictionary_name.data = dictionary_entry.dictionary_name
        dictionary_form.description.data = dictionary_entry.description

    return render_template('main/edit_dictionary.html',
                           title=dictionary_entry.dictionary_name,
                           dictionary=dictionary_entry,
                           form=dictionary_form)


@bp.route('/word/<int:word_id>')
@login_required
def word(word_id):
    word_entry = Word.query.filter_by(id=word_id).first_or_404()
    return render_template('main/word.html',
                           title=word_entry.spelling,
                           word=word_entry)


@bp.route('/check_dictionary_name', methods=['POST'])
def check_dictionary_name():
    dictionary_name = request.form['dictionary_name']
    dictionary_entry = Dictionary.query.filter_by(dictionary_name=dictionary_name).first()
    return jsonify({'name_available': dictionary_entry is None})


@bp.route('/add_word', methods=['POST'])
def add_word():
    new_word = Word(
        spelling=request.form['spelling'].strip(),
        definition=request.form['definition'].strip(),
        dictionary_id=request.form['dictionary_id'])
    db.session.add(new_word)
    db.session.commit()

    return jsonify({'new_word_id': new_word.id})


@bp.route('/delete_word', methods=['POST'])
def delete_word():
    word_entry = Word.query.filter_by(id=request.form['word_id']).first_or_404()
    db.session.delete(word_entry)
    db.session.commit()

    return jsonify({'success': True})


@bp.route('/save_word', methods=['POST'])
def save_word():
    word_entry = Word.query.filter_by(id=request.form['word_id']).first_or_404()
    word_entry.spelling = request.form['spelling'].strip()
    word_entry.definition = request.form['definition'].strip()
    db.session.commit()

    return jsonify({'success': True})


@bp.route('/games', methods=['GET'])
@login_required
def games():
    if request.method == 'GET':
        revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
        show_previous_game = (revision_game_entry is not None and not revision_game_entry.game_completed)

        return render_template('main/games.html', title='Games', show_previous_game=show_previous_game)


@bp.route('/game/<game_parameter>', methods=['GET', 'POST'])
@login_required
def game(game_parameter):
    """
    param game_parameter:
        Continue - resume previous game
        FindDefinition - start new game
        FindSpelling - start new game

    """
    if request.method == 'GET':
        game_type = GameType.FindDefinition
        revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
        revision_game = None
        game_rounds = []
        new_game = False
        if game_parameter == 'Continue':
            revision_game = RevisionGame(GameType[revision_game_entry.game_type], [])
            revision_game.load_game_rounds(json.loads(revision_game_entry.game_data))
            revision_game.current_round = revision_game_entry.current_round
            revision_game.total_rounds = revision_game_entry.total_rounds
        elif game_parameter == 'Remove':
            if revision_game_entry is not None:
                db.session.delete(revision_game_entry)
                db.session.commit()
            return redirect(url_for('main.games'))
        else:
            game_type = GameType[game_parameter]
            new_game = True

        if new_game:
            if revision_game_entry is not None:
                db.session.delete(revision_game_entry)
                db.session.commit()

            word_limit = 5
            words_query = Word.query.order_by(func.random()).limit(7).all()
            revision_game = GameGenerator.generate_game(words_query, game_type, word_limit)
            revision_game_entry = CurrentGame()
            revision_game_entry.game_type = game_type.name
            revision_game_entry.game_data = json.dumps(revision_game.to_json())
            revision_game_entry.user_id = current_user.id
            revision_game_entry.total_rounds = revision_game.total_rounds
            revision_game_entry.current_round = 0
            db.session.add(revision_game_entry)
            db.session.commit()

        if revision_game is not None:
            game_rounds = revision_game.game_rounds

        return render_template('main/game.html',
                               title='RevisionGame',
                               game_type=game_type,
                               game_rounds=game_rounds)

    if request.method == 'POST':
        # End of a game
        pass


logger = logging.getLogger(__name__)

