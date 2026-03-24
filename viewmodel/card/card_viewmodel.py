from common.observable import Observable
from common.relay_command import RelayCommand
from model.card.card import Card

class CardViewModel(Observable):
    def __init__(self, card: Card):
        super().__init__()
        self._card = card
        self._is_highlighted = False
        self.long_press_command = RelayCommand(self._on_long_press)

    @property
    def name(self):
        return self._card.name

    @property
    def allowed_spaces(self):
        return self._card.allowed_action_spaces

    @property
    def is_highlighted(self):
        return self._is_highlighted

    @is_highlighted.setter
    def is_highlighted(self, value):
        if self._is_highlighted != value:
            self._is_highlighted = value
            self._notify('is_highlighted', not value, value)

    def _on_long_press(self, param):
        # 触发地图高亮，传递本卡牌
        from viewmodel.map.map_viewmodel import MapViewModel
        map_vm = MapViewModel.get_instance()
        if map_vm:
            map_vm.highlight_regions_by_allowed_spaces(self.allowed_spaces)
        # 同时需要通知视图开始拖拽特使，由 View 层处理