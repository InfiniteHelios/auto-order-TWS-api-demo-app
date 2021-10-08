from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QCheckBox
from models.main_model import mainModel
from models.order_entry_model import OrderEntryModel
from ui.order_entry_ui import Ui_OrderEntry


class OrderEntryController(QObject):
    def __init__(self, model: OrderEntryModel, ui: Ui_OrderEntry):
        super().__init__()
        self._mainModel = mainModel
        self._model = model
        self._ui = ui
        self.init_connection()

    def init_connection(self):
        self._model.app.accounts_loaded.connect(self.on_accounts_loaded)

    @pyqtSlot(list)
    def on_accounts_loaded(self, accounts: list):
        self._mainModel.accounts = accounts
        for account in accounts:
            chkAccount = QCheckBox(account)
            self._ui.layTicker.addWidget(chkAccount)
