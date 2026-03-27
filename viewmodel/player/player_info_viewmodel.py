from common.observable import Observable
from common.relay_command import RelayCommand
from model.player.player import Player
from viewmodel.card.hand_viewmodel import HandViewModel


class PlayerInfoViewModel(Observable):
    def __init__(self, player: Player, hand_viewmodel: HandViewModel):
        super().__init__()
        self._player = player
        self._hand_vm = hand_viewmodel
        self._show_hand_command = RelayCommand(self._show_hand)

    # ---------- 属性 ----------
    @property
    def name(self) -> str:
        return self._player.name

    @property
    def resources(self):
        return self._player.resources

    @property
    def envoy_count(self) -> int:
        return self._player.envoy_count

    # ---------- 命令 ----------
    @property
    def show_hand_command(self) -> RelayCommand:
        return self._show_hand_command

    def _show_hand(self, param=None):
        """点击时，将手牌区切换到该玩家的手牌"""
        self._hand_vm.set_display_player(self._player.id)

    # ---------- 资源更新 ----------
    def update_resources(self):
        self._notify('resources', None, self.resources)
        self._notify('envoy_count', None, self.envoy_count)