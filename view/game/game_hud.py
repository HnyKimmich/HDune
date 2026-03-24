from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from viewmodel.game.game_hud_viewmodel import GameHUDViewModel

class GameHUD(QWidget):
    def __init__(self, viewmodel: GameHUDViewModel, player_id: int, parent=None):
        super().__init__(parent)
        self._vm = viewmodel
        self._player_id = player_id
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
        # 使用 Observable 机制，假设 ViewModel 的 _notify 会调用注册的监听器
        # 这里简单使用自定义回调，或使用 Qt 信号槽（推荐）
        # 我们可以在 ViewModel 中发射 Qt 信号，但为了保持简单，这里假设 Observable 的 on_property_changed 方法。
        # 实际上，你的 Observable 可能没有 Qt 信号，需要手动轮询或使用信号。
        # 这里为了演示，直接使用一个定时器或属性变更检查，但最好改为信号。
        # 更合理的方式是：让 GameHUDViewModel 继承 QObject 并使用 pyqtSignal，这样可以直接连接。
        # 为了代码完整，我们假设 GameHUDViewModel 已经支持 Qt 信号（需要修改），但你的 Observable 是普通 Python 类。
        # 你可以修改 GameHUDViewModel 使其同时继承 QObject 和 Observable，并发出自定义信号。
        # 为简化，这里不展开，假设已实现信号。
        pass

    def on_show_clicked(self):
        success, msg = self._vm.show_card(self._player_id)
        if not success:
            # 显示错误
            pass
        else:
            # 更新状态
            pass

    def update_display(self, phase: str, round_num: int, player_name: str, conflict_card: str):
        self.phase_label.setText(f"阶段: {phase}")
        self.round_label.setText(f"回合: {round_num}")
        self.player_label.setText(f"当前玩家: {player_name}")
        self.conflict_label.setText(f"冲突卡: {conflict_card or '无'}")