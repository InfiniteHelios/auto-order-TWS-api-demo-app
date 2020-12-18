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

    def actionUpdated(self, isSell: bool):
        self._mainModel.action = 'Sell' if isSell else 'Buy'

    def validation_check(self):
        self._model.entryLevelData = self._ui.groupEntryLevel._model.data
        self._model.pt1Data = self._ui.groupPT1._model.data
        self._model.pt2Data = self._ui.groupPT2._model.data
        self._model.pt3Data = self._ui.groupPT3._model.data
        self._model.pt4Data = self._ui.groupPT4._model.data
        return self._model.validation_check()
