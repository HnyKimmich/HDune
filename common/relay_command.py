# RelayCommand 实现（占位）
class RelayCommand:
    def __init__(self, func):
        self._func = func
    def execute(self, *args, **kwargs):
        return self._func(*args, **kwargs)
