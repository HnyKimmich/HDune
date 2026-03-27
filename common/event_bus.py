from typing import Dict, List, Callable, Any

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def publish(self, event_name: str, data: Any = None):
        if event_name in self._subscribers:
            for cb in self._subscribers[event_name]:
                cb(data)

# 事件名称常量
EVENT_CURRENT_PLAYER_CHANGED = "current_player_changed"
EVENT_PHASE_CHANGED = "phase_changed"
EVENT_ACTION_PHASE_ENDED = "action_phase_ended"