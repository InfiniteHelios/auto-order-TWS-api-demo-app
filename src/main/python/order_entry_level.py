from PyQt5.QtWidgets import QGroupBox
from controllers.order_entry_level_controller import OrderEntryLevelController
from models.order_entry_level_model import OrderEntryLevelModel
from ui.order_entry_level_ui import Ui_OrderEntryLevel


class OrderEntryLevel(QGroupBox, Ui_OrderEntryLevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_Ui()

        self._model = OrderEntryLevelModel()
        self._controller = OrderEntryLevelController(self._model, self._ui)

        self.init_connection()

    def __del__(self):
        del self._controller
        del self._model

    def init_Ui(self):
        self._ui = Ui_OrderEntryLevel()
        self._ui.setupUi(self)
        self.setEnabled(False)

    def init_connection(self):
        pass
