from PyQt5.QtCore import QObject, pyqtSlot
from models.order_entry_level_model import OrderEntryLevelModel
from ui.order_entry_level_ui import Ui_OrderEntryLevel


class OrderEntryLevelController(QObject):
    def __init__(self, model: OrderEntryLevelModel, ui: Ui_OrderEntryLevel):
        super().__init__()
        self._model = model
        self._ui = ui
        self.init_connection()

    def init_connection(self):
        pass
