from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from viewmodel.game.game_hud_viewmodel import GameHUDViewModel

class GameHUD(QWidget):
    def __init__(self, viewmodel: GameHUDViewModel, parent=None):
        super().__init__(parent)
        self._vm = viewmodel
        self._init_ui()
        self._bind_viewmodel()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.phase_label = QLabel()
        self.round_label = QLabel()
        self.player_label = QLabel()
        self.conflict_label = QLabel()
        self.show_button = QPushButton("展示")
        self.show_button.clicked.connect(self.on_show_clicked)

        layout.addWidget(self.phase_label)
        layout.addWidget(self.round_label)
        layout.addWidget(self.player_label)
        layout.addWidget(self.conflict_label)
        layout.addWidget(self.show_button)
        self.setLayout(layout)

    def _bind_viewmodel(self):
        # 绑定属性变化，更新 UI 显示
        self._vm.on_property_changed('current_phase', self._on_phase_changed)
        self._vm.on_property_changed('round_number', self._on_round_changed)
        self._vm.on_property_changed('current_player_name', self._on_player_changed)
        self._vm.on_property_changed('conflict_card_name', self._on_conflict_changed)

        # 初始显示
        self._on_phase_changed(None, self._vm.current_phase)
        self._on_round_changed(None, self._vm.round_number)
        self._on_player_changed(None, self._vm.current_player_name)
        self._on_conflict_changed(None, self._vm.conflict_card_name)

    def _on_phase_changed(self, _, new_phase):
        self.phase_label.setText(f"阶段: {new_phase}")

    def _on_round_changed(self, _, new_round):
        self.round_label.setText(f"回合: {new_round}")

    def _on_player_changed(self, _, new_player):
        self.player_label.setText(f"当前玩家: {new_player}")

    def _on_conflict_changed(self, _, new_card):
        self.conflict_label.setText(f"冲突卡: {new_card or '无'}")

    def on_show_clicked(self):
        success, msg = self._vm.show_card()
        if not success:
            QMessageBox.warning(self, "提示", msg)
        else:
            # 可选：显示成功信息（如状态栏）
            pass