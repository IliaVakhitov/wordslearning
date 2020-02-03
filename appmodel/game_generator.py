import logging
import random
from typing import List, Optional

from app.models import Word
from appmodel.revision_game import RevisionGame
from appmodel.game_round import GameRound
from appmodel.game_type import GameType


class GameGenerator:

    """
    Class is used to generate list of GameRounds
    """

    @staticmethod
    def mix_list(item_list) -> List:
        """
        Function allows to mix elements in list
        :param item_list: initial list
        :return: List - new mixed list
        """

        list_length = len(item_list)
        tmp_list = item_list.copy()
        new_list = []
        for i in range(list_length):
            new_list.append(
                tmp_list.pop(
                    random.randint(0, len(tmp_list) - 1)))

        return new_list

    @staticmethod
    def get_random_definition(
            all_words: List[Word],
            used_value: str,
            used_values: List[str]) -> str:
        """
        Function allows to get random translation or spelling from given list of DictEntries
        :param all_words: Source list of DictionaryEntries
        :param used_value: correct answer. This value will be ignored
        :param used_values: this values will be ignored
        :return: str translation
        """

        new_word = all_words[random.randint(0, len(all_words) - 1)]
        while new_word.definition == used_value or new_word.definition in used_values:
            new_word = all_words[random.randint(0, len(all_words) - 1)]

        return new_word.definition

    @staticmethod
    def get_random_spelling(
            all_words: List[Word],
            used_value: str,
            used_values: List[str]) -> str:
        """
        Function allows to get random translation or spelling from given list of DictEntries
        :param all_words: Source list of DictionaryEntries
        :param used_value: correct answer. This value will be ignored
        :param used_values: this values will be ignored
        :return: str spelling
        """

        new_word = all_words[random.randint(0, len(all_words) - 1)]
        while new_word.spelling == used_value or new_word.spelling in used_values:
            new_word = all_words[random.randint(0, len(all_words) - 1)]

        return new_word.spelling

    @staticmethod
    def game_find_spelling(
            words_list: List[Word],
            words_limit: int) -> Optional[List[GameRound]]:
        """
        Generates list of GameRounds
        :param words_list: list to generate game rounds
        :param words_limit: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            List of GameRounds:
        """

        game_rounds: List[GameRound] = []

        for next_word in words_list:
            # For each entry generating 3 random spellings
            # Correct answer inserted before getting random values

            if 0 < words_limit <= len(game_rounds):
                break

            # index for correct answer
            correct_index = random.randint(0, 3)

            correct_spelling = next_word.spelling
            spellings = []
            for i in range(3):
                spellings.append(
                    GameGenerator.get_random_spelling(
                        words_list, correct_spelling, spellings))

            spellings.insert(correct_index, correct_spelling)

            # New game round
            round_data = {}
            round_data['word_id'] = next_word.id
            round_data['value'] = next_word.definition
            round_data['answers'] = spellings
            round_data['correct_index'] = correct_index
            round_data['learning_index_id'] = 0 \
                if next_word.learning_index is None \
                else next_word.learning_index.id

            round_data['learning_index_value'] = 0 \
                if next_word.learning_index is None \
                else next_word.learning_index.index

            game_rounds.append(GameRound(round_data))

        logger.info(f'Game generated, round {len(game_rounds)}, type Find Spelling')
        return game_rounds

    @staticmethod
    def game_find_definition(
            words_list: List[Word],
            words_limit: int) -> Optional[List[GameRound]]:
        """
        Generates list of GameRounds
        Does not make sense if words_number < 4. Return None in this case
        :param words_list: list to generate game rounds
        :param words_limit: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            List of GameRounds:
        """

        game_rounds: List[GameRound] = []

        for next_word in words_list:
            # For each entry generating 3 random spellings
            # Correct answer inserted before getting random values

            if 0 < words_limit <= len(game_rounds):
                break

            # index for correct answer
            correct_index = random.randint(0, 3)

            correct_definition = next_word.definition
            definitions = []
            for i in range(3):
                definitions.append(
                    GameGenerator.get_random_definition(
                        words_list, correct_definition, definitions))

            definitions.insert(correct_index, correct_definition)

            # New game round. Index + 1 [1-4]
            round_data = {}
            round_data['word_id'] = next_word.id
            round_data['value'] = next_word.spelling
            round_data['answers'] = definitions
            round_data['correct_index'] = correct_index
            round_data['learning_index_id'] = 0 \
                if next_word.learning_index is None \
                else next_word.learning_index.id

            round_data['learning_index_value'] = 0 \
                if next_word.learning_index is None \
                else next_word.learning_index.index

            game_rounds.append(GameRound(round_data))

        logger.info(f'Game generated, round {len(game_rounds)}, type Find Definition')
        return game_rounds

    @staticmethod
    def generate_game(
            words_list: List[Word],
            game_type: GameType,
            words_limit: int = 0) -> Optional[RevisionGame]:
        """
        Generates list of GameRounds
        Does not make sense if words_number < 4. Return None in this case
        :param words_list: list to generate game rounds
        :param game_type: enum
        :param words_limit: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            instance of RevisionGame
        """

        if len(words_list) == 0:
            # No words in dictionaries
            logger.info('No words in dictionaries!')
            return None

        if len(words_list) < 4:
            logger.info('Not enough words to generate game!')
            return None

        logger.info('Generating game')
        if game_type == GameType.FindDefinition:
            return RevisionGame(game_type, GameGenerator.game_find_definition(words_list, words_limit))
        elif game_type == GameType.FindSpelling:
            return RevisionGame(game_type, GameGenerator.game_find_spelling(words_list, words_limit))


logger = logging.getLogger(__name__)

