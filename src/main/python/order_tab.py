from PyQt5.QtWidgets import QWidget
from ui.order_tab_ui import Ui_OrderTab


class OrderTab(QWidget, Ui_OrderTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_Ui()

    def init_Ui(self):
        self._ui = Ui_OrderTab()
        self._ui.setupUi(self)
