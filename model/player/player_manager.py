from typing import List, Optional
from .player import Player

class PlayerManager:
    def __init__(self, players: List[Player]):
        self.players = players
        self.current_player_index = 0

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_player_by_id(self, pid: int) -> Optional[Player]:
        for p in self.players:
            if p.id == pid:
                return p
        return None