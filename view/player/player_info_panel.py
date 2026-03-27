from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from viewmodel.player.player_info_viewmodel import PlayerInfoViewModel


class PlayerInfoPanel(QWidget):
    def __init__(self, viewmodel: PlayerInfoViewModel, parent=None):
        super().__init__(parent)
        self._vm = viewmodel
        self.setFixedSize(200, 150)
        self.setStyleSheet("border: 1px solid black; background: #f0f0f0;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_label = QLabel(self._vm.name)
        layout.addWidget(self.name_label)

        self.resources_label = QLabel()
        self.envoy_label = QLabel()
        self._update_labels()
        layout.addWidget(self.resources_label)
        layout.addWidget(self.envoy_label)

        # 添加查看手牌的按钮
        self.show_hand_btn = QPushButton("查看手牌")
        self.show_hand_btn.clicked.connect(self._vm.show_hand_command.execute)
        layout.addWidget(self.show_hand_btn)

        # 监听资源变化
        self._vm.on_property_changed('resources', self._on_resources_changed)
        self._vm.on_property_changed('envoy_count', self._on_envoy_changed)

    def _update_labels(self):
        res = self._vm.resources
        text = f"水: {res['water']}  香料: {res['spice']}\n钱: {res['solari']}  军队: {res['army']}"
        self.resources_label.setText(text)
        self.envoy_label.setText(f"特使: {self._vm.envoy_count}")

    def _on_resources_changed(self, old, new):
        self._update_labels()

    def _on_envoy_changed(self, old, new):
        self.envoy_label.setText(f"特使: {new}")