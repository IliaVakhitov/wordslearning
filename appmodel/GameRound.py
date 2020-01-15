import json
from typing import List, Dict
from app.models import Word, LearningIndex


class GameRound:
    """
    Contains word and 4 different translations to guess
    Correct answer and correct answer`s index [1-4] for fast check
    """

    def __init__(self,
                 word: Word,
                 value: str,
                 answers: List[str],
                 correct_answer: str,
                 correct_index: int,
                 learning_index: LearningIndex):

        self.word_id: int = word.id
        self.value: str = value
        self.answer1: str = answers[0]
        self.answer2: str = answers[1]
        self.answer3: str = answers[2]
        self.answer4: str = answers[3]
        self.correct_answer: str = correct_answer
        self.correct_index: int = correct_index
        self.learning_index_id: int = 0 if learning_index is None else learning_index.id
        self.learning_index_value: int = 0 if learning_index is None else learning_index.index
        self.new_learning_index_value: int = 0 if learning_index is None else learning_index.index
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

    def to_json(self) -> Dict:
        json_data = {
            'word_id': self.word_id,
            'value': self.value,
            'answer1': self.answer1,
            'answer2': self.answer2,
            'answer3': self.answer3,
            'answer4': self.answer4,
            'correct_answer': self.correct_answer,
            'correct_index': self.correct_index,
            'learning_index_id': self.learning_index_id,
            'learning_index_value': self.learning_index_value,
            'new_learning_index_value': self.new_learning_index_value,
            'learning_index_changed': self.learning_index_changed
        }

        return json_data

    def load_from_json(self, json_data) -> bool:
        try:
            self.word_id = json_data['word_id']
            self.value = json_data['value']
            self.answer1 = json_data['answer1']
            self.answer2 = json_data['answer2']
            self.answer3 = json_data['answer3']
            self.answer4 = json_data['answer4']
            self.correct_answer = json_data['correct_answer']
            self.correct_index = json_data['correct_index']
            self.learning_index_id = json_data['learning_index_id']
            self.learning_index_value = json_data['learning_index_value']
            self.new_learning_index_value = json_data['new_learning_index_value']
            self.learning_index_changed = json_data['learning_index_changed']

            return True
        except:
            # TODO add logder.error
            return False


