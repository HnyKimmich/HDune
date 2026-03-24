from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Card:
    id: str
    name: str
    card_type: str                # 原 JSON 中的 "type"
    allowed_action_spaces: List[str]
    play_effects: List[Dict[str, Any]]
    show_effects: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Card':
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            card_type=data.get('type', 'None'),
            allowed_action_spaces=data.get('allowed_action_spaces', []),
            play_effects=data.get('play_effects', []),
            show_effects=data.get('show_effects', [])
        )