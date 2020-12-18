from PyQt5.QtCore import QObject
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

    def stopLossUpdated(self, stopLoss: int):
        self._model.stopLoss = stopLoss
        self._ui.spnLoss.setValue(self._model.loss)

    def stopLossPriceUpdated(self, stopLossPrice: float):
        self._model.stopLossPrice = stopLossPrice
        self._ui.spnLoss.setValue(self._model.loss)

    def thresholdUpdated(self, threshold: float):
        self._model.threshold = threshold
        self._ui.spnThresholdPrice.setValue(self._model.thresholdPrice)

    def posUpdated(self, pos: int):
        self._model.pos = pos
        self._ui.spnLoss.setValue(self._model.loss)
        self._ui.spnThresholdPrice.setValue(self._model.thresholdPrice)

    def priceUpdated(self, price: float):
        self._model.price = price
        self._ui.spnLoss.setValue(self._model.loss)
        self._ui.spnThresholdPrice.setValue(self._model.thresholdPrice)
