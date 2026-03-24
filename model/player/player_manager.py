from typing import List, Optional
from .player import Player

class PlayerManager:
    def __init__(self, players: List[Player]):
        self.players = players
        self.current_player_index = 0

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_turn(self):
        # 回合结束清理
        current = self.current_player
        current.deck_controller.end_turn()
        # 切换玩家
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        # 新玩家抽牌
        self.current_player.draw_cards(5)

    def get_player_by_id(self, pid: int) -> Optional[Player]:
        for p in self.players:
            if p.id == pid:
                return p
        return None