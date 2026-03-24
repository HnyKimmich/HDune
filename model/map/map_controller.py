import json
from pathlib import Path
from typing import List, Optional, Callable
from .region import Region

class MapController:
    def __init__(self):
        self.regions: List[Region] = []

    def load_from_json(self, file_path: Path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.regions = [Region.from_dict(item) for item in data]

    def get_region_by_name(self, name: str) -> Optional[Region]:
        for r in self.regions:
            if r.name == name:
                return r
        return None

    def get_all_regions(self) -> List[Region]:
        return self.regions

    def set_envoy_change_callback(self, callback: Callable[[str, int], None]):
        """设置特使变化回调，参数为 (region_name, player_id)"""
        self._envoy_change_callback = callback

    def place_envoy(self, region_name: str, player_id: int) -> bool:
        region = self.get_region_by_name(region_name)
        if not region:
            return False
        region.envoy_owner = player_id
        # 通知回调
        if self._envoy_change_callback:
            self._envoy_change_callback(region_name, player_id)
        return True

    def remove_envoy(self, region_name: str):
        region = self.get_region_by_name(region_name)
        if region:
            region.envoy_owner = None
            if self._envoy_change_callback:
                self._envoy_change_callback(region_name, None)  # 可选，传 None 
