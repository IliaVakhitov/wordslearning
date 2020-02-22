import json
import logging
from flask_login import login_required, current_user
from flask import render_template, flash, jsonify
from flask import url_for
from flask import request
from flask import redirect
from sqlalchemy import func

from app.games import bp
from app import db
from app.games.forms import GameParametersForm
from app.models import CurrentGame, Word, Dictionary, Statistic, LearningIndex
from appmodel.game_generator import GameGenerator
from appmodel.game_type import GameType


@bp.route('/define_game', methods=['GET', 'POST'])
@login_required
def define_game():
    game_form = GameParametersForm()
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
    dictionaries = Dictionary.query.filter_by(user_id=current_user.id).order_by('dictionary_name')

    if 'resume' in request.form:
        # If game completed
        if revision_game_entry is not None and revision_game_entry.game_completed:
            return redirect(url_for('games.game_statistic'))
        return redirect(url_for('games.play_game'))

    if 'remove' in request.form:
        if revision_game_entry is not None:
            db.session.delete(revision_game_entry)
            db.session.commit()
        return redirect(url_for('games.define_game'))

    if game_form.validate_on_submit():
        # Remove previous game
        if revision_game_entry is not None:
            db.session.delete(revision_game_entry)
            db.session.commit()

        # Game parameters from page
        game_type = GameType[request.form['game_type'].strip()]
        word_limit = int(request.form['game_rounds'].strip())
        not_include_learned_words = (request.form['include_learned_words'].strip() == "False")

        # In need to filter dictionaries
        if 'select_dictionaries' in request.form:
            dict_names = request.form.getlist('select_dictionaries')
            dictionaries = Dictionary.query.\
                filter_by(user_id=current_user.id).\
                filter(Dictionary.dictionary_name.in_(dict_names)).\
                order_by('dictionary_name')

        # IDs need to make filter in words query
        dict_ids = [d.id for d in dictionaries]
        words_query = db.session.query(Word).filter(Word.dictionary_id.in_(dict_ids))

        if not_include_learned_words:
            words_query = words_query.\
                join(LearningIndex, LearningIndex.word_id == Word.id).\
                filter(LearningIndex.index < 100)

        # Getting random order and limit is defined
        words_query = words_query.order_by(func.random()).limit(word_limit).all()

        # Generate game from given list of words
        revision_game = GameGenerator.generate_game(words_query, game_type)
        if revision_game is None:
            logger.info('Could not create game!')
            flash('Could not create game! Not enough words to create game! Try to add dictionaries!')
            return redirect(url_for('games.define_game'))

        # Entry of current game to continue if not finished
        revision_game_entry = CurrentGame()
        revision_game_entry.game_type = game_type.name
        revision_game_entry.game_data = json.dumps(revision_game.to_json())
        revision_game_entry.user_id = current_user.id
        revision_game_entry.total_rounds = revision_game.total_rounds
        revision_game_entry.current_round = 0
        db.session.add(revision_game_entry)
        db.session.commit()

        return redirect(url_for('games.play_game'))

    show_previous_game = (revision_game_entry is not None and not revision_game_entry.game_completed)

    return render_template('games/define_game.html',
                           title='Games',
                           show_previous_game=show_previous_game,
                           dictionaries=dictionaries,
                           form=game_form)


@bp.route('/next_round', methods=['POST'])
@login_required
def next_round():
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
    game_ended = revision_game_entry.get_next_round()
    if game_ended:
        return jsonify({'redirect': url_for('games.game_statistic')})
    return revision_game_entry.get_current_round()


@bp.route('/current_round', methods=['POST'])
@login_required
def current_round():
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
    return revision_game_entry.get_current_round()


@bp.route('/get_correct_index', methods=['POST'])
@login_required
def get_correct_index():
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
    return jsonify({'correct_index': revision_game_entry.get_correct_index(request.form['answer_index']),
                   'progress': revision_game_entry.get_progress()})


@bp.route('/game_statistic/', methods=['GET'])
@login_required
def game_statistic():
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=True).first()
    total_rounds = revision_game_entry.total_rounds
    correct_answers = revision_game_entry.correct_answers

    # Update statistic table
    statistic_entry = Statistic(user_id=current_user.id)
    statistic_entry.game_type = revision_game_entry.game_type
    statistic_entry.total_rounds = total_rounds
    statistic_entry.correct_answers = correct_answers

    db.session.add(statistic_entry)
    db.session.delete(revision_game_entry)
    db.session.commit()

    return render_template('games/game_statistic.html',
                           total_rounds=total_rounds,
                           correct_answers=correct_answers)


@bp.route('/play_game/', methods=['GET'])
@login_required
def play_game():
    return render_template('games/play_game.html',
                               title='Revision Game')


logger = logging.getLogger(__name__)

