
class DictionaryEntry:

    """ Dictionary entry
            word - word in foreign language ,
            translation  - in native language
            learn index - int in range [0,100]
    """

    def __init__(self, spelling: str, definition: str, learning_index: int) -> None:
        self.spelling = spelling
        self.definition = definition
        self.learning_index = learning_index if learning_index > 0 else 0

    def set_learn_index(self, value) -> None:
        if value < 0:
            self.learning_index = 0
        elif value >= 100:
            self.learning_index = 100
        else:
            self.learning_index = value

    def increase_learn_index(self) -> None:
        self.learning_index += (5 if self.learning_index < 100 else 0)

    def decrease_learn_index(self) -> None:
        self.learning_index -= (5 if self.learning_index > 0 else 0)

