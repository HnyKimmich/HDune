from common.observable import Observable

class PlayerInfoViewModel(Observable):
    def __init__(self, player):
        super().__init__()
        self._player = player

    @property
    def name(self):
        return self._player.name

    @property
    def resources(self):
        return self._player.resources

    @property
    def envoy_count(self):
        return self._player.envoy_count

    def update_resources(self):
        self._notify('resources', None, self.resources)
        self._notify('envoy_count', None, self.envoy_count)