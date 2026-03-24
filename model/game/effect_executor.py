from typing import Optional, List
from ..player.player import Player
from ..player.player_manager import PlayerManager
from ..card.card import Card
from ..map.region import Region
from ..effect.factory import EffectFactory
from .conflict_controller import ConflictController

class EffectExecutor:
    def __init__(self, effect_factory: EffectFactory):
        self.effect_factory = effect_factory

    def execute_effects(self, effect_data_list: List[Dict], player: Player, region: Region = None):
        for effect_data in effect_data_list:
            effect = self.effect_factory.create(effect_data)
            if effect:
                effect.execute(player, region)