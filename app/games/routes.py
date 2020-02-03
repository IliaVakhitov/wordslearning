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
from app.models import CurrentGame, Word, Dictionary
from appmodel.game_generator import GameGenerator
from appmodel.game_round import GameRound
from appmodel.game_type import GameType
from appmodel.revision_game import RevisionGame


@bp.route('/define', methods=['GET'])
@login_required
def define():
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()
    show_previous_game = (revision_game_entry is not None
                          and not revision_game_entry.game_completed
                          and revision_game_entry.total_rounds > revision_game_entry.current_round)

    return render_template('games/define_game.html', title='Games', show_previous_game=show_previous_game)


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
    return jsonify({'correct_index': revision_game_entry.get_correct_index(request.form['answer_index'])})


@bp.route('/game_statistic/', methods=['GET'])
@login_required
def game_statistic():
    revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=True).first()
    total_rounds = revision_game_entry.total_rounds
    correct_answers = revision_game_entry.correct_answers
    # TODO update statistic table
    db.session.delete(revision_game_entry)
    db.session.commit()

    return render_template('games/game_statistic.html',
                           total_rounds=total_rounds,
                           correct_answers=correct_answers)


@bp.route('/play/<game_parameter>', methods=['GET'])
@login_required
def play_game(game_parameter):
    """
    param game_parameter:
        Continue - resume previous game
        FindDefinition - start new game
        FindSpelling - start new game

    """
    # TODO split function in several
    if request.method == 'GET':
        game_type = GameType.FindDefinition
        revision_game_entry = CurrentGame.query.filter_by(user_id=current_user.id, game_completed=False).first()

        revision_game = None
        game_rounds = []
        new_game = False
        if game_parameter == 'Continue':
            if revision_game_entry is not None and revision_game_entry.game_completed:
                return redirect(url_for('games.game_statistic'))
            game_type = GameType[revision_game_entry.game_type]
        elif game_parameter == 'Remove':
            if revision_game_entry is not None:
                db.session.delete(revision_game_entry)
                db.session.commit()
            return redirect(url_for('games.define'))

        elif game_parameter == 'FindDefinition':
            game_type = GameType[game_parameter]
            new_game = True
        elif game_parameter == 'FindSpelling':
            game_type = GameType[game_parameter]
            new_game = True
        elif game_parameter == 'End_Game':
            return redirect(url_for('games.game_statistic'))

        if new_game:
            if revision_game_entry is not None:
                db.session.delete(revision_game_entry)
                db.session.commit()
            # TODO get a game parameter
            word_limit = 5
            dictionaries = Dictionary.query.filter_by(user_id=current_user.id).all()
            dict_ids = [d.id for d in dictionaries]
            words_query = Word.query.\
                filter(Word.dictionary_id.in_(dict_ids)).\
                order_by(func.random()).\
                limit(word_limit).all()
            revision_game = GameGenerator.generate_game(words_query, game_type, word_limit)
            if revision_game is None:
                logger.info('Could not create game!')
                flash('Could not create game!')
                return redirect(url_for('games.define'))

            revision_game_entry = CurrentGame()
            revision_game_entry.game_type = game_type.name
            revision_game_entry.game_data = json.dumps(revision_game.to_json())
            revision_game_entry.user_id = current_user.id
            revision_game_entry.total_rounds = revision_game.total_rounds
            revision_game_entry.current_round = 0
            db.session.add(revision_game_entry)
            db.session.commit()

        return render_template('games/play_game.html',
                               title='Revision Game',
                               game_type=game_type)


logger = logging.getLogger(__name__)

