from typing import Optional, List
from ..player.player import Player
from ..player.player_manager import PlayerManager
from ..card.card import Card
from ..map.region import Region
from ..effect.factory import EffectFactory
from .conflict_controller import ConflictController

class GameRuleService:
    def __init__(self, effect_factory: EffectFactory, conflict_controller: ConflictController):
        self.effect_factory = effect_factory
        self.conflict_controller = conflict_controller
        self.winner = None
        self.win_score = 11

    def check_winner(self, players: List[Player]) -> Optional[Player]:
        for p in players:
            # 假设胜利分数由资源中的“胜利点”表示（可扩展）
            if p.resources.get('victory_points', 0) >= self.win_score:
                self.winner = p
                return p
        return None

    def can_play_card_to_region(self, player: Player, card: Card, region: Region) -> bool:
        # 资源检查占位
        if not self._check_resources(player, card, region):
            return False
        if not card.allowed_action_spaces:
            return False
        return region.allowed_action_space in card.allowed_action_spaces

    def _check_resources(self, player: Player, card: Card, region: Region) -> bool:
        # 后续实现
        return True