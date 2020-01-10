from typing import List

from app.models import Word
from appmodel.DictionaryEntry import DictionaryEntry


class GameRound:
    """
    Contains word and 4 different translations to guess
    Correct answer and correct answer`s index [1-4] for fast check
    """

    def __init__(self,
                 word: DictionaryEntry,
                 value: str,
                 answers: List[str],
                 correct_answer: str,
                 correct_index: int,
                 learning_index: int):

        self.dictionary_entry: DictionaryEntry = word
        self.value: str = value
        self.answer1: str = answers[0]
        self.answer2: str = answers[1]
        self.answer3: str = answers[2]
        self.answer4: str = answers[3]
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

        return_str = self.value + "\n"
        return_str += "1. " + self.answer1 + "\n"
        return_str += "2. " + self.answer2 + "\n"
        return_str += "3. " + self.answer3 + "\n"
        return_str += "4. " + self.answer4

        return return_str

    def print_game_round_with_answer(self) -> str:

        return_str = self.print_game_round()
        return_str += "Correct {} - {} ".format(self.correct_answer, self.correct_index)

        return return_str
