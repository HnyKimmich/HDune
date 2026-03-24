from dataclasses import dataclass, field
from typing import List, Dict, Any
from typing import Optional

@dataclass
class Region:
    name: str
    allowed_action_space: str
    effect: List[Dict[str, Any]]
    cost: List[Dict[str, Any]]
    envoy_owner: Optional[int] = None   # 新增：特使所属玩家ID，None表示无特使

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Region':
        return cls(
            name=data.get('name', ''),
            allowed_action_space=data.get('allowed_action_space', ''),
            effect=data.get('effect', []),
            cost=data.get('cost', [])
        )