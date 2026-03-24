from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt
from .map.map_view import MapView
from .card.hand_view import HandView
from .player.player_info_panel import PlayerInfoPanel
from .game.game_hud import GameHUD

class MainWindow(QMainWindow):
    def __init__(self, map_view: MapView, hand_view: HandView, player_panels: list, game_hud: GameHUD):
        super().__init__()
        self.setWindowTitle("桌游原型")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 顶部 HUD
        main_layout.addWidget(game_hud)

        # 中间：地图 + 左侧玩家列表
        middle_splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        for panel in player_panels:
            left_layout.addWidget(panel)
        left_layout.addStretch()
        middle_splitter.addWidget(left_widget)
        middle_splitter.addWidget(map_view)
        middle_splitter.setSizes([300, 900])
        main_layout.addWidget(middle_splitter)

        # 底部手牌
        main_layout.addWidget(hand_view)