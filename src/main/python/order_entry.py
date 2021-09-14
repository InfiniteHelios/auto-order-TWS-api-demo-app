from PyQt5.QtWidgets import QWidget

from ui.order_entry_ui import Ui_OrderEntry


class OrderEntry(QWidget, Ui_OrderEntry):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
