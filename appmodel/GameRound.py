import json
from typing import List, Dict
from app.models import Word, LearningIndex


class GameRound:
    """
    Contains word and 4 different translations to guess
    Correct answer and correct answer`s index [1-4] for fast check
    """

    def __init__(self, dict_data: Dict):

        self.word_id: int = dict_data.get('word_id')
        self.value: str = dict_data.get('value')
        self.answers: List[str] = dict_data.get('answers')
        self.correct_index: int = dict_data.get('correct_index')
        self.correct_answer: str = self.answers[self.correct_index]
        self.learning_index_id: int = dict_data.get('learning_index_id')
        self.learning_index_value: int = dict_data.get('learning_index_value')
        self.new_learning_index_value: int = dict_data.get('learning_index_value')
        self.learning_index_changed: bool = False

    @staticmethod
    def fill_from_dict(dict_data: Dict):
        return GameRound(dict_data)

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


