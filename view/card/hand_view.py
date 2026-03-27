from PyQt5.QtWidgets import QWidget, QHBoxLayout
from viewmodel.card.hand_viewmodel import HandViewModel
from viewmodel.card.card_viewmodel import CardViewModel
from .card_view import CardView


class HandView(QWidget):
    """手牌视图，绑定 HandViewModel"""
    def __init__(self, viewmodel: HandViewModel, parent=None):
        super().__init__(parent)
        self._vm = viewmodel
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self._card_views = []

        # 监听手牌变化
        self._vm.on_property_changed('hand_cards', self._on_hand_cards_changed)
        self._refresh_cards()

    def _refresh_cards(self):
        """根据 ViewModel 的 hand_cards 刷新视图"""
        # 清除现有卡片
        for cv in self._card_views:
            cv.deleteLater()
        self._card_views.clear()

        # 创建新卡片
        for card in self._vm.hand_cards:
            # 创建 CardViewModel 实例
            card_vm = CardViewModel(card)   # CardViewModel 接收 Card 对象
            card_view = CardView(card_vm)   # CardView 接收 CardViewModel
            self.layout.addWidget(card_view)
            self._card_views.append(card_view)

    def _on_hand_cards_changed(self, old, new):
        self._refresh_cards()