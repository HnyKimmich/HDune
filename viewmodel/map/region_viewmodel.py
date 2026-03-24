from common.observable import Observable
from common.relay_command import RelayCommand
from model.map.region import Region

class RegionViewModel(Observable):
    def __init__(self, region: Region, on_drop_callback=None):
        super().__init__()
        self.region = region
        self._is_highlighted = False
        self.on_drop_callback = on_drop_callback
        self.drop_command = RelayCommand(self._on_drop)

    @property
    def name(self):
        return self.region.name

    @property
    def is_highlighted(self):
        return self._is_highlighted

    @property
    def envoy_owner(self):
        return self.region.envoy_owner

    @property
    def has_envoy(self):
        return self.region.envoy_owner is not None

    @is_highlighted.setter
    def is_highlighted(self, value):
        if self._is_highlighted != value:
            self._is_highlighted = value
            self._notify('is_highlighted', not value, value)
    
    @property
    def envoy_owner(self):
        return self.region.envoy_owner

    @envoy_owner.setter
    def envoy_owner(self, value):
        if self.region.envoy_owner != value:
            old = self.region.envoy_owner
            self.region.envoy_owner = value
            self._notify('envoy_owner', old, value)

    @property
    def has_envoy(self):
        return self.region.envoy_owner is not None

    def _on_drop(self, param):
        if self.on_drop_callback:
            self.on_drop_callback(param, self.region)

    