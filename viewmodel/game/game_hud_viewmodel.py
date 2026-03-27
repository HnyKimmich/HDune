# viewmodel/game/game_hud_viewmodel.py
from common.observable import Observable
from common.event_bus import EventBus, EVENT_PHASE_CHANGED, EVENT_CURRENT_PLAYER_CHANGED, EVENT_ACTION_PHASE_ENDED
from model.game.turn_controller import TurnController, GamePhase
from model.game.conflict_controller import ConflictController

class GameHUDViewModel(Observable):
    def __init__(self, turn_controller: TurnController, conflict_controller: ConflictController, event_bus: EventBus):
        super().__init__()
        self.turn_controller = turn_controller
        self.conflict_controller = conflict_controller
        self._event_bus = event_bus
        self._current_phase = turn_controller.phase
        self._current_player_index = turn_controller.current_action_player_index
        self._current_player_name = turn_controller.player_manager.players[self._current_player_index].name
        self._conflict_card_name = None

        # 订阅事件
        event_bus.subscribe(EVENT_PHASE_CHANGED, self._on_phase_changed)
        event_bus.subscribe(EVENT_CURRENT_PLAYER_CHANGED, self._on_current_player_changed)
        event_bus.subscribe(EVENT_ACTION_PHASE_ENDED, self._on_action_phase_ended)

        if self.conflict_controller.current_conflict:
            self._conflict_card_name = self.conflict_controller.current_conflict.name

    def _on_phase_changed(self, phase: GamePhase):
        self._current_phase = phase
        self._notify('current_phase', None, phase.value)

    def _on_current_player_changed(self, player_index: int):
        self._current_player_index = player_index
        player_name = self.turn_controller.player_manager.players[player_index].name
        self._current_player_name = player_name
        self._notify('current_player_name', None, player_name)

    def _on_action_phase_ended(self, _=None):
        # 可做额外处理
        pass

    @property
    def current_phase(self):
        return self._current_phase.value

    @property
    def round_number(self):
        return self.turn_controller.round

    @property
    def current_player_name(self):
        return self._current_player_name

    @property
    def conflict_card_name(self):
        return self._conflict_card_name

    def update_conflict_card(self):
        if self.conflict_controller.current_conflict:
            self._conflict_card_name = self.conflict_controller.current_conflict.name
            self._notify('conflict_card_name', None, self._conflict_card_name)

    # 暴露给 UI 的命令
    def show_card(self):
        """当前玩家执行展示"""
        return self.turn_controller.action_phase_player_show()

    def play_card(self, card, target_region_name: str = None):
        """当前玩家打出卡牌"""
        return self.turn_controller.action_phase_player_play(card, target_region_name)