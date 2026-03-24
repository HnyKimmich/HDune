from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from .card_view import CardView

class HandView(QWidget):
    def __init__(self, hand_viewmodels: list, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self._card_views = []
        self.update_hand(hand_viewmodels)

    def update_hand(self, new_viewmodels):
        for cv in self._card_views:
            cv.deleteLater()
        self._card_views.clear()
        for vm in new_viewmodels:
            card_view = CardView(vm)
            self.layout.addWidget(card_view)
            self._card_views.append(card_view)

    def _on_show(self):
        # 通知 ViewModel 展示所有手牌
        # 需要连接到外部的信号或通过事件总线
        pass