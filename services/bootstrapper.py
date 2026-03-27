import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication

from model.card.card_library import CardLibrary
from model.card.deck_controller import DeckController
from model.effect.factory import SimpleEffectFactory
from model.map.map_controller import MapController
from model.player.player import Player
from model.player.player_manager import PlayerManager
from model.game.game_rule_service import GameRuleService
from model.game.conflict_controller import ConflictController
from model.game.turn_controller import TurnController

from viewmodel.card.card_viewmodel import CardViewModel
from viewmodel.card.hand_viewmodel import HandViewModel
from viewmodel.map.map_viewmodel import MapViewModel
from viewmodel.player.player_info_viewmodel import PlayerInfoViewModel
from viewmodel.game.game_hud_viewmodel import GameHUDViewModel

from view.main_window import MainWindow
from view.map.map_view import MapView
from view.card.hand_view import HandView
from view.player.player_info_panel import PlayerInfoPanel
from view.game.game_hud import GameHUD

from common.event_bus import EventBus, EVENT_CURRENT_PLAYER_CHANGED

# 全局单例引用（用于拖拽传递）
_current_player = None
_current_card_vm = None
_game_rule_service = None
_current_player = None
_current_card_vm = None

def set_current_player(player):
    global _current_player
    _current_player = player

def set_current_card_vm(vm):
    global _current_card_vm
    _current_card_vm = vm

def clear_current_card_vm():
    global _current_card_vm
    _current_card_vm = None

def get_current_player():
    return _current_player

def get_current_card_vm():
    return _current_card_vm

def get_game_rule_service():
    return _game_rule_service

class Bootstrapper:
    @staticmethod
    def run():
        app = QApplication(sys.argv)

        # 创建事件总线
        event_bus = EventBus()

        # 1. 加载数据
        card_lib = CardLibrary()
        card_lib.load_from_json(Path("data/cards/initial_cards.json"))
        all_cards = card_lib.get_all_cards()
        initial_deck = []
        card_names = ["外交", "寻求盟友", "实验", "实验", "说服", "说服", "印章戒指", "侦察", "匕首", "匕首"]
        for name in card_names:
            card = card_lib.get_card_by_name(name)
            if card:
                initial_deck.append(card)

        # 地图
        map_controller = MapController()
        map_controller.load_from_json(Path("data/maps/default_map.json"))

        # 创建4个玩家
        players = []
        for i in range(4):
            deck = DeckController(initial_deck.copy())
            player = Player(i, f"玩家{i}", deck)
            player.resources = {'water': 1, 'spice': 0, 'solari': 0, 'army': 3}
            players.append(player)

        player_manager = PlayerManager(players)

        # 冲突控制器
        conflict_controller = ConflictController()
        conflict_controller.load_conflict_deck(Path("data/cards/conflict_cards.json"))

        # 效果工厂
        effect_factory = SimpleEffectFactory()

        # 游戏规则服务
        game_rule_service = GameRuleService(effect_factory, conflict_controller)

        # 回合控制器，传入 map_controller 和 event_bus
        turn_controller = TurnController(player_manager, conflict_controller, game_rule_service, map_controller, event_bus)

        # 为了全局拖拽，监听当前玩家变化并更新全局变量
        def on_current_player_changed(player_index):
            set_current_player(turn_controller.player_manager.players[player_index])
        event_bus.subscribe(EVENT_CURRENT_PLAYER_CHANGED, on_current_player_changed)

        # 启动第一回合
        turn_controller.start_round()

        # 创建 ViewModel
        hud_vm = GameHUDViewModel(turn_controller, conflict_controller, event_bus)

        # 创建 HandViewModel
        hand_vm = HandViewModel(player_manager, turn_controller, event_bus)

        # 创建 PlayerInfoViewModel，传入 hand_vm
        player_info_vms = [PlayerInfoViewModel(p, hand_vm) for p in players]

        # 创建 MapViewModel，传入 turn_controller 和 map_controller，并设置特使变化回调
        map_vm = MapViewModel(map_controller, turn_controller)
        map_controller.set_envoy_change_callback(lambda region_name, player_id: map_vm.update_region_envoy(region_name, player_id))

        # 3. View
        map_view = MapView(map_vm)
        hand_view = HandView(hand_vm)
        player_panels = [PlayerInfoPanel(vm) for vm in player_info_vms]
        game_hud = GameHUD(hud_vm)

        # 将全局引用绑定（用于拖拽）
        global _current_player, _current_card_vm
        _current_player = player_manager.current_player

        global _game_rule_service
        _game_rule_service = game_rule_service

        # 4. 主窗口
        main_win = MainWindow(map_view, hand_view, player_panels, game_hud)
        main_win.show()

        sys.exit(app.exec_())