from typing import List

from app.models import Word


class GameRound:
    """
    Contains word and 4 different translations to guess
    Correct answer and correct answer`s index [1-4] for fast check
    """

    def __init__(self,
                 word: Word,
                 spelling: str,
                 translations: List[str],
                 correct_answer: str,
                 correct_index: int,
                 learning_index: int):

        self.dictionary_entry: Word = word
        self.spelling: str = spelling
        self.translation1: str = translations[0]
        self.translation2: str = translations[1]
        self.translation3: str = translations[2]
        self.translation4: str = translations[3]
        self.correct_answer: str = correct_answer
        self.correct_index: int = correct_index
        self.learning_index: int = learning_index
        self.new_learning_index: int = learning_index
        self.learning_index_changed: bool = False

    def is_answer_correct(self, answer) -> bool:

        return answer == self.correct_answer

    def is_index_correct(self, index) -> bool:

        return index == self.correct_index

    def print_game_round(self) -> str:

        return_str = self.spelling + "\n"
        return_str += "1. " + self.translation1 + "\n"
        return_str += "2. " + self.translation2 + "\n"
        return_str += "3. " + self.translation3 + "\n"
        return_str += "4. " + self.translation4

        return return_str

    def print_game_round_with_answer(self) -> str:

        return_str = self.print_game_round()
        return_str += "Correct {} - {} ".format(self.correct_answer, self.correct_index)

        return return_str
