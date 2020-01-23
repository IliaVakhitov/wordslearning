import json
from typing import List, Dict

from appmodel.game_round import GameRound
from appmodel.game_type import GameType


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
            json_data['game_rounds'].append(json.dumps(game_round.__dict__))

        return json_data

    def load_game_rounds(self, json_data):
        self.game_rounds.clear()
        for game_round_data in json_data['game_rounds']:
            self.game_rounds.append(GameRound(json.loads(game_round_data)))


