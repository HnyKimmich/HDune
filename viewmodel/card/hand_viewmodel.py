from typing import List, Optional
from common.observable import Observable
from common.relay_command import RelayCommand
from common.event_bus import EventBus, EVENT_CURRENT_PLAYER_CHANGED
from model.player.player_manager import PlayerManager
from model.game.turn_controller import TurnController
from model.card.card import Card


class HandViewModel(Observable):
    """手牌面板 ViewModel"""
    def __init__(self, player_manager: PlayerManager, turn_controller: TurnController, event_bus: EventBus):
        super().__init__()
        self._player_manager = player_manager
        self._turn_controller = turn_controller
        self._event_bus = event_bus
        self._display_player_id = turn_controller.current_action_player_index
        self._play_card_command = RelayCommand(self._play_card, self._can_play_card)

        # 订阅事件
        event_bus.subscribe(EVENT_CURRENT_PLAYER_CHANGED, self._on_current_player_changed)

    # ---------- 公共属性 ----------
    @property
    def display_player_id(self) -> int:
        return self._display_player_id

    @property
    def hand_cards(self) -> List[Card]:
        player = self._player_manager.get_player_by_id(self._display_player_id)
        return player.hand_cards if player else []

    @property
    def is_current_player(self) -> bool:
        """当前显示的玩家是否是当前行动玩家"""
        return (self._display_player_id ==
                self._turn_controller.current_action_player_index)

    # ---------- 公共方法 ----------
    def set_display_player(self, player_id: int):
        """切换显示哪个玩家的手牌（供其他玩家面板调用）"""
        if self._display_player_id != player_id:
            self._display_player_id = player_id
            self._notify("hand_cards", None, self.hand_cards)

    def _on_current_player_changed(self, new_player_index: int):
        """回合切换时自动切回当前玩家的手牌"""
        self.set_display_player(new_player_index)

    # ---------- 命令 ----------
    @property
    def play_card_command(self) -> RelayCommand:
        return self._play_card_command

    def _can_play_card(self, card: Card) -> bool:
        # 只有当手牌区显示的是当前行动玩家时，才允许出牌
        return self.is_current_player

    def _play_card(self, card: Card):
        if not self._can_play_card(card):
            return
        # 调用回合控制器的出牌逻辑（假设默认目标区域为 None）
        success, msg = self._turn_controller.action_phase_player_play(card, None)
        if not success:
            # 可以在这里通知错误消息，通过事件总线或回调
            print(f"出牌失败: {msg}")
        else:
            # 出牌成功后，手牌列表已变化，触发刷新
            self._notify("hand_cards", None, self.hand_cards)