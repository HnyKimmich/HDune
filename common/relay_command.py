from typing import Callable, Optional, Any

class RelayCommand:
    def __init__(self, execute: Callable[[Any], None], can_execute: Optional[Callable[[Any], bool]] = None):
        self._execute = execute
        self._can_execute = can_execute

    def execute(self, param: Any = None):
        if self.can_execute(param):
            return self._execute(param)

    def can_execute(self, param: Any = None) -> bool:
        if self._can_execute is None:
            return True
        return self._can_execute(param)

    def raise_can_execute_changed(self):
        # 可选：触发 CanExecuteChanged 事件（用于 UI 更新）
        pass