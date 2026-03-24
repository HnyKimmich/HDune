from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from viewmodel.map.region_viewmodel import RegionViewModel

class RegionView(QWidget):   # 改为 QWidget 以便布局
    def __init__(self, viewmodel: RegionViewModel, parent=None):
        super().__init__(parent)
        self._vm = viewmodel
        self.setFixedSize(120, 80)
        self.setAcceptDrops(True)

        # 创建布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 区域名称标签
        self.name_label = QLabel(viewmodel.name)
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)

        # 特使图标（初始隐藏）
        self.envoy_icon = QLabel()
        self.envoy_icon.setFixedSize(30, 30)
        self.envoy_icon.setAlignment(Qt.AlignCenter)
        self.envoy_icon.setStyleSheet("background-color: red; border-radius: 15px;")
        self.envoy_icon.hide()
        layout.addWidget(self.envoy_icon, alignment=Qt.AlignCenter)

        self._update_style()
        self._vm.on_property_changed('is_highlighted', self._on_highlight_changed)
        # 监听 envoy_owner 变化（需要在 ViewModel 中添加属性变化通知）
        self._vm.on_property_changed('envoy_owner', self._on_envoy_changed)

    def _update_style(self):
        if self._vm.is_highlighted:
            self.setStyleSheet("background-color: lightgreen; border: 2px solid green;")
        else:
            self.setStyleSheet("background-color: beige; border: 1px solid gray;")

    def _on_highlight_changed(self, old, new):
        self._update_style()

    def _on_envoy_changed(self, old, new):
        if self._vm.has_envoy:
            self.envoy_icon.show()
        else:
            self.envoy_icon.hide()

    # dragEnterEvent / dropEvent 保持不变

    def dragEnterEvent(self, event: QDragEnterEvent):
        if self._vm.is_highlighted:
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        from services.bootstrapper import get_current_player, get_current_card_vm, clear_current_card_vm
        card_vm = get_current_card_vm()
        player = get_current_player()
        self._vm.drop_command.execute((card_vm, player))
        # 可选清除
        clear_current_card_vm()
        event.acceptProposedAction()