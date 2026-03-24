from abc import ABC, abstractmethod
from typing import Any, Dict

class IEffect(ABC):
    @abstractmethod
    def execute(self, context: 'EffectContext') -> None:
        """执行效果，context 包含玩家、目标区域、卡牌等信息"""
        pass