import logging
import random
from typing import List, Optional

from appmodel.GameRound import GameRound
from appmodel.GameType import GameType
from app.models import Word

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
        :param all_words: Source list of DictEntries
        :param used_value: correct answer. This value is ignored
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
        :param all_words: Source list of DictEntries
        :param used_value: correct answer. This value is ignored
        :param used_values: this values will be ignored
        :return: str spelling
        """

        new_word = all_words[random.randint(0, len(all_words) - 1)]
        while new_word.spelling == used_value or new_word.spelling in used_values:
            new_word = all_words[random.randint(0, len(all_words) - 1)]

        return new_word.spelling

    @staticmethod
    def generate_game(
            words_list: List[Word],
            game_type: GameType,
            words_number: int = 0) -> Optional[List[GameRound]]:

        """
        Generates list of GameRounds
        Does not make sense if words_number < 4. Return None in this case
        :param words_list: list to generate game rounds
        :param game_type: enum
        :param words_number: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            List of GameRounds
        """

        if len(words_list) == 0:
            # No words in dictionaries
            logging.info("No words in dictionaries!")
            return None

        if len(words_list) < 4:
            logging.info("Not enough words to generate game!")
            return None

        if game_type == GameType.FindTranslation:
            return GameGenerator.game_find_translation(words_list, words_number)
        elif game_type == GameType.FindSpelling:
            return GameGenerator.game_find_spelling(words_list, words_number)

    @staticmethod
    def game_find_spelling(
            words_list: List[Word],
            words_number: int) -> Optional[List[GameRound]]:

        """
        Generates list of GameRounds
        :param words_list: list to generate game rounds
        :param words_number: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            List of GameRounds:
        """

        game_rounds: List[GameRound] = []

        all_words = GameGenerator.mix_list(words_list)
        for next_word in all_words:
            # For each entry generating 3 random spellings
            # Correct answer inserted before getting random values

            if 0 < words_number <= len(game_rounds):
                break

            # index for correct answer
            correct_index = random.randint(0, 3)

            value = next_word.spelling
            translations = []
            for i in range(3):
                translations.append(
                    GameGenerator.get_random_definition(
                        all_words, value, translations))

            translations.insert(correct_index, value)
            # New game round. Index + 1 [1-4]
            game_rounds.append(
                GameRound(
                    next_word,
                    next_word.translation,
                    translations,
                    next_word.spelling,
                    correct_index + 1,
                    next_word.learning_index
                ))

        return game_rounds

    @staticmethod
    def game_find_translation(
            words_list: List[Word],
            words_number: int) -> Optional[List[GameRound]]:

        """
        Generates list of GameRounds
        Does not make sense if words_number < 4. Return None in this case
        :param words_list: list to generate game rounds
        :param words_number: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            List of GameRounds:
        """

        game_rounds: List[GameRound] = []

        all_words = GameGenerator.mix_list(words_list)
        for next_word in all_words:
            # For each entry generating 3 random spellings
            # Correct answer inserted before getting random values

            if 0 < words_number <= len(game_rounds):
                break

            # index for correct answer
            correct_index = random.randint(0, 3)

            value = next_word.translation
            spellings = []
            for i in range(3):
                spellings.append(
                    GameGenerator.get_random_spelling(
                        all_words, value, spellings))

            spellings.insert(correct_index, value)
            # New game round. Index + 1 [1-4]
            game_rounds.append(
                GameRound(
                    next_word,
                    next_word.spelling,
                    spellings,
                    next_word.translation,
                    correct_index + 1,
                    next_word.learning_index
                ))

        return game_rounds
