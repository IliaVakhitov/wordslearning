import logging
from typing import List

from sqlalchemy.sql.expression import func
from app.models import Word
from appmodel.DictionaryEntry import DictionaryEntry
from appmodel.GameGenerator import GameGenerator
from appmodel.GameType import GameType


class GameManager:

    def get_game_rounds(self, game_type: GameType, word_limit: int):
        words_query = Word.query.order_by(func.random()).limit(word_limit).all()
        logger.info(type(words_query))
        words_list: List[DictionaryEntry] = list()
        for word_entry in words_query:
            # DEBUG
            logger.info(word_entry.spelling)
            logger.info(word_entry.definition)

            words_list.append(
                DictionaryEntry(
                    word_entry.spelling,
                    word_entry.definition,
                    0)) # TODO word_entry.learning_index.index))

        result = GameGenerator.generate_game(words_list, game_type, word_limit)
        return result


logger = logging.getLogger(__name__)

