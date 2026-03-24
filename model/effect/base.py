from abc import ABC, abstractmethod
from typing import Any, Dict

class IEffect(ABC):
    @abstractmethod
    def execute(self, player, region) -> None:
        """执行效果，修改游戏状态"""
        pass

class EffectFactory(ABC):
    @abstractmethod
    def create(self, effect_data: Dict[str, Any]) -> IEffect:
        pass