from PyQt5.QtWidgets import QWidget
from models.order_entry_model import OrderEntryModel
from controllers.order_entry_controller import OrderEntryController
from ui.order_entry_ui import Ui_OrderEntry


class OrderEntry(QWidget, Ui_OrderEntry):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_Ui()

        self._model = OrderEntryModel()
        self._controller = OrderEntryController(self._model, self._ui)

        self.init_connection()

    def __del__(self):
        del self._controller
        del self._model
        pass

    def init_Ui(self):
        self._ui = Ui_OrderEntry()
        self._ui.setupUi(self)
        self.setEnabled(False)

    def init_connection(self):
        pass
