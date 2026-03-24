from typing import Callable, Dict, List

class Observable:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def on_property_changed(self, property_name: str, handler: Callable):
        """注册属性变化监听器"""
        if property_name not in self._handlers:
            self._handlers[property_name] = []
        self._handlers[property_name].append(handler)

    def _notify(self, property_name: str, old_value, new_value):
        """通知所有监听器属性已变化"""
        if property_name in self._handlers:
            for handler in self._handlers[property_name]:
                handler(old_value, new_value)