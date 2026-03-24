from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class ConflictCard:
    name: str
    rewards: List[Dict[str, Any]]   # 例如 [{"rank": 1, "resource": "water", "amount": 2}, ...]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConflictCard':
        return cls(
            name=data.get('name', ''),
            rewards=data.get('rewards', [])
        )