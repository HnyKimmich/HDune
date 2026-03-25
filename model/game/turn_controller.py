from enum import Enum
from typing import List, Optional, Callable
from ..player.player import Player
from ..player.player_manager import PlayerManager
from .conflict_controller import ConflictController
from .game_rule_service import GameRuleService

class GamePhase(Enum):
    PREPARE = "准备阶段"
    ACTION = "行动阶段"
    CONFLICT = "冲突阶段"
    END = "回合结束"

class TurnController:
    def __init__(self, player_manager: PlayerManager, conflict_controller: ConflictController,
                 game_rule_service: GameRuleService, map_controller):
        self.player_manager = player_manager
        self.conflict_controller = conflict_controller
        self.rule_service = game_rule_service
        self.map_controller = map_controller
        self.phase = GamePhase.PREPARE
        self.round = 1
        self.current_action_player_index = 0
        self._phase_changed_callbacks: List[Callable[[GamePhase], None]] = []
        self._current_player_changed_callbacks: List[Callable[[int], None]] = []
        self._action_phase_ended_callbacks: List[Callable[[], None]] = []

    def register_phase_changed(self, callback: Callable[[GamePhase], None]):
        self._phase_changed_callbacks.append(callback)

    def register_current_player_changed(self, callback: Callable[[int], None]):
        self._current_player_changed_callbacks.append(callback)

    def register_action_phase_ended(self, callback: Callable[[], None]):
        self._action_phase_ended_callbacks.append(callback)

    def _notify_phase_changed(self):
        for cb in self._phase_changed_callbacks:
            cb(self.phase)

    def _notify_current_player_changed(self):
        for cb in self._current_player_changed_callbacks:
            cb(self.current_action_player_index)

    def _notify_action_phase_ended(self):
        for cb in self._action_phase_ended_callbacks:
            cb()

    def start_round(self):
        self.phase = GamePhase.PREPARE
        self._notify_phase_changed()
        self.round += 1
        self.conflict_controller.draw_conflict_card()
        for player in self.player_manager.players:
            player.draw_cards(5)
            player.act_done = False
        self.current_action_player_index = self.player_manager.current_player_index
        self.phase = GamePhase.ACTION
        self._notify_phase_changed()
        self._notify_current_player_changed()

    def action_phase_player_play(self, card, target_region_name: str = None):
        """当前玩家打出一张卡牌到目标区域"""
        player = self.player_manager.players[self.current_action_player_index]
        if player.act_done:
            return False, "当前玩家已行动完成，不能继续行动"

        success, msg = player.play_card(card, target_region_name)
        if not success:
            return False, msg

        if target_region_name and self.map_controller:
            self.map_controller.place_envoy(target_region_name, player.id)

        print(f"玩家 {player.id} 成功打出 {card.name} 到 {target_region_name}")

        if all(p.act_done for p in self.player_manager.players):
            self._end_action_phase()
            return True, "所有玩家已完成行动，进入冲突阶段"
        else:
            self._next_active_player()
            self._notify_current_player_changed()
            print(f"轮到玩家 {self.current_action_player_index}")
            return True, f"轮到下一玩家"

    def action_phase_player_show(self):
        """当前玩家执行展示动作"""
        player = self.player_manager.players[self.current_action_player_index]
        if player.act_done:
            return False, "当前玩家已行动完成，不能重复展示"

        player.show_all_hand()
        player.act_done = True

        print(f"玩家 {player.id} 进行展示")
        for p in self.player_manager.players:
            print(f"玩家{p.id}的展示状态是{p.act_done}")

        if all(p.act_done for p in self.player_manager.players):
            print("所有玩家已完成行动，进入冲突阶段")
            self._end_action_phase()
            return True, "所有玩家已完成行动，进入冲突阶段"
        else:
            self._next_active_player()
            self._notify_current_player_changed()
            print(f"轮到玩家 {self.current_action_player_index}")
            return True, f"轮到下一玩家"

    def _next_active_player(self):
        players = self.player_manager.players
        start = (self.current_action_player_index + 1) % len(players)
        idx = start
        while True:
            if not players[idx].act_done:
                self.current_action_player_index = idx
                return
            idx = (idx + 1) % len(players)
            if idx == start:
                break

    def _end_action_phase(self):
        self.phase = GamePhase.CONFLICT
        self._notify_phase_changed()
        self.resolve_conflict()
        self._notify_action_phase_ended()

    def resolve_conflict(self):
        powers = {}
        for player in self.player_manager.players:
            powers[player.id] = player.resources.get('army', 0)
        rewards = self.conflict_controller.resolve_conflict(powers)
        for pid, reward_list in rewards.items():
            player = self.player_manager.get_player_by_id(pid)
            if reward_list:
                for reward in reward_list:
                    res_name = reward.get('resource')
                    amount = int(reward.get('amount', 0))
                    if res_name in player.resources:
                        player.resources[res_name] += amount
        self.phase = GamePhase.END
        self._notify_phase_changed()

    def end_round(self):
        for player in self.player_manager.players:
            player.restore_envoy()
            player.reset_turn_status()
            if hasattr(player, '_show_done'):
                delattr(player, '_show_done')
        self.player_manager.current_player_index = (self.player_manager.current_player_index + 1) % len(self.player_manager.players)
        self.current_action_player_index = self.player_manager.current_player_index
        winner = self.rule_service.check_winner(self.player_manager.players)
        if winner:
            self.phase = GamePhase.END
            self._notify_phase_changed()
            return winner
        self.start_round()
        return None