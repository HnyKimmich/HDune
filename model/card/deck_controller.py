import random
from typing import List, Optional
from .card import Card

class DeckController:
    def __init__(self, initial_cards: List[Card]):
        self.draw_pile = initial_cards.copy()
        self.discard_pile: List[Card] = []
        self.played_pile: List[Card] = []
        self.shuffle_draw_pile()

    def shuffle_draw_pile(self):
        random.shuffle(self.draw_pile)

    def draw_cards(self, count: int) -> List[Card]:
        drawn = []
        for _ in range(count):
            if not self.draw_pile:
                self._reshuffle_discard_into_draw()
                if not self.draw_pile:
                    break   # 无牌可抽
            drawn.append(self.draw_pile.pop())
        return drawn

    def _reshuffle_discard_into_draw(self):
        if not self.discard_pile:
            return
        self.draw_pile = self.discard_pile
        self.discard_pile = []
        self.shuffle_draw_pile()

    def discard_cards(self, cards: List[Card]):
        self.discard_pile.extend(cards)

    def add_to_played(self, cards: List[Card]):
        self.played_pile.extend(cards)

    def end_turn(self):
        # 回合结束：打出牌堆 → 弃牌堆
        self.discard_pile.extend(self.played_pile)
        self.played_pile.clear()