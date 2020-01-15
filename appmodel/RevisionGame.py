from typing import List, Dict

from appmodel.GameRound import GameRound
from appmodel.GameType import GameType


class RevisionGame:

    def __init__(self, game_type: GameType, game_rounds: List[GameRound]):
        self.game_rounds: List[GameRound] = game_rounds
        self.game_type: GameType = game_type
        self.total_rounds: int = len(game_rounds)
        self.current_round = 0
        self.is_completed = False

    def to_json(self) -> Dict:
        json_data = {'game_rounds': []}
        for game_round in self.game_rounds:
            json_data['game_rounds'].append({f'game_round{self.game_rounds.index(game_round)}': game_round.to_json()})

        return json_data

    def load_game_rounds(self, json_data):
        pass


