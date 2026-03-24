# model/player/player.py
from typing import List, Optional, Tuple
from ..card.card import Card
from ..card.deck_controller import DeckController

class Player:
    def __init__(self, player_id: int, name: str, deck_controller: DeckController):
        self.id = player_id
        self.name = name
        self.resources = {'water': 0, 'spice': 0, 'solari': 0, 'army': 0}
        self.deck_controller = deck_controller
        self.hand_cards: List[Card] = []
        self.envoy_count = 2
        self.act_done = False          # 新增：本行动阶段是否已完成
        # 特使阶段状态（预留）
        self.envoy_phase_active = False

    def draw_initial_hand(self, count: int = 5):
        self.hand_cards = self.deck_controller.draw_cards(count)

    def draw_cards(self, count: int):
        drawn = self.deck_controller.draw_cards(count)
        self.hand_cards.extend(drawn)
        return drawn

    def play_card(self, card: Card, target_region_name: str = None) -> Tuple[bool, str]:
        """打出手牌，返回 (成功, 消息)"""
        if self.envoy_count <= 0:
            return False, "没有可用的特使"
        if card not in self.hand_cards:
            return False, "手牌中没有该卡牌"
        self.hand_cards.remove(card)
        self.deck_controller.add_to_played([card])
        self.envoy_count -= 1
        # 注意：这里可以返回更详细的成功信息，例如放置区域等
        return True, f"成功打出 {card.name}"

    def show_all_hand(self) -> List[Card]:
        """展示所有手牌，返回展示的牌列表"""
        if not self.hand_cards:
            return []
        shown_cards = self.hand_cards.copy()
        self.deck_controller.add_to_played(shown_cards)
        self.hand_cards.clear()
        return shown_cards

    def restore_envoy(self):
        self.envoy_count = 2

    def reset_turn_status(self):
        self.act_done = False
        self.envoy_phase_active = False
        # 其他临时状态重置