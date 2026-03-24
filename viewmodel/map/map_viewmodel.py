from typing import List, Set
from common.observable import Observable
from .region_viewmodel import RegionViewModel
from model.map.map_controller import MapController

class MapViewModel(Observable):
    _instance = None

    def __new__(cls, map_controller: MapController = None, turn_controller=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, map_controller: MapController = None, turn_controller=None):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._map_controller = map_controller
        self._turn_controller = turn_controller
        self.region_viewmodels: List[RegionViewModel] = []
        self._highlighted_region_names: Set[str] = set()

        for region in self._map_controller.get_all_regions():
            rvm = RegionViewModel(region, on_drop_callback=self._on_card_dropped)
            self.region_viewmodels.append(rvm)

    @classmethod
    def get_instance(cls):
        return cls._instance

    def _on_card_dropped(self, param, region):
        card_vm, player = param
        success, msg = self._turn_controller.action_phase_player_play(
            player.id, card_vm._card, region.name
        )
        # 可在此将消息发送到侧边栏
        return success, msg

    def highlight_regions_by_allowed_spaces(self, allowed_spaces: List[str]):
        self.clear_highlight()
        for rvm in self.region_viewmodels:
            if rvm.region.allowed_action_space in allowed_spaces:
                rvm.is_highlighted = True
                self._highlighted_region_names.add(rvm.region.name)

    def update_region_envoy(self, region_name: str, player_id: int):
        rvm = self.get_region_viewmodel_by_name(region_name)
        if rvm:
            rvm.envoy_owner = player_id

    def clear_highlight(self):
        for rvm in self.region_viewmodels:
            rvm.is_highlighted = False
        self._highlighted_region_names.clear()

    def get_region_viewmodel_by_name(self, name: str):
        for rvm in self.region_viewmodels:
            if rvm.region.name == name:
                return rvm
        return None