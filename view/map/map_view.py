from PyQt5.QtWidgets import QWidget, QGridLayout
from .region_view import RegionView

class MapView(QWidget):
    def __init__(self, map_viewmodel, parent=None):
        super().__init__(parent)
        self._vm = map_viewmodel
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self._region_views = []
        # 简单布局，将区域排成网格（实际可按坐标排）
        for i, rvm in enumerate(self._vm.region_viewmodels):
            view = RegionView(rvm)
            self.layout.addWidget(view, i // 3, i % 3)
            self._region_views.append(view)