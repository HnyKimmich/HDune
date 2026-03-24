import json
from typing import Dict, List
from pathlib import Path
from .card import Card

class CardLibrary:
    _instance = None
    _cards: Dict[str, Card] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_from_json(self, file_path: Path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for card_data in data:
            card = Card.from_dict(card_data)
            self._cards[card.name] = card   # 用 name 作为临时 id，后续可改为唯一 id

    def get_card_by_name(self, name: str) -> Card:
        return self._cards.get(name)

    def get_all_cards(self) -> List[Card]:
        return list(self._cards.values())