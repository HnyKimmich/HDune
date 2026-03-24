# view/card/card_view.py
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint, QMimeData
from PyQt5.QtGui import QPixmap, QDrag
from viewmodel.card.card_viewmodel import CardViewModel

class CardView(QLabel):
    def __init__(self, viewmodel: CardViewModel, parent=None):
        super().__init__(parent)
        self._vm = viewmodel
        self.setText(viewmodel.name)
        self.setFixedSize(100, 140)
        self.setStyleSheet("border: 1px solid black; background: lightgray;")
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            from viewmodel.map.map_viewmodel import MapViewModel
            map_vm = MapViewModel.get_instance()
            if map_vm:
                map_vm.highlight_regions_by_allowed_spaces(self._vm.allowed_spaces)
            from services.bootstrapper import set_current_card_vm, get_current_player
            current_player = get_current_player()
            if current_player:
                set_current_card_vm(self._vm)
            self._start_drag()

    def _start_drag(self):
        drag = QDrag(self)
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.red)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(25, 25))
        mime_data = QMimeData()
        mime_data.setText(self._vm.name)
        drag.setMimeData(mime_data)

        # 执行拖拽（阻塞，直到释放）
        drag.exec_(Qt.CopyAction)

        # 拖拽结束，清除高亮
        from viewmodel.map.map_viewmodel import MapViewModel
        MapViewModel.get_instance().clear_highlight()
        # 可选：清除全局变量
        from services.bootstrapper import clear_current_card_vm
        clear_current_card_vm()