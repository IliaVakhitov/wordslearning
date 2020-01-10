from enum import Enum


class GameType(Enum):
    FindDefinition = 'Find Definition'
    FindSpelling = 'Find Spelling'

    def __str__(self):
        return f'{self.value}'

