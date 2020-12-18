from PyQt5.QtCore import QObject
from ui.order_entry_level_ui import Ui_OrderEntryLevel


class OrderEntryLevelModel(QObject):
    def __init__(self, ui: Ui_OrderEntryLevel):
        super().__init__()
        self._ui = ui
        self.loadInitialModel()

    def __del__(self):
        pass

    def loadInitialModel(self):
        self._pos: int = self._ui.spnPos.value()
        self._price: float = self._ui.spnPrice.value()
        self._stopLoss: int = self._ui.cmbStopLoss.currentData()
        self._stopLossPrice: float = self._ui.spnStopLossPrice.value()
        self._threshold: int = self._ui.spnThreshold.value()
        self._mode = 'Percentage'
        self.calcAllPrices()

    def calcAllPrices(self):
        self.calcLoss()
        self.calcThresholdPrice()

    def calcLoss(self, isFixedMode: bool = False):
        self._mode = 'Fixed' if isFixedMode else 'Percentage'
        self._loss = self._price * self._pos * self._stopLoss / 100.0 if not isFixedMode \
            else self._pos * (self._price - self._stopLossPrice)

    @property
    def data(self):
        return {
            'POS': self._pos,
            'Price': self._price,
            'Mode': self._mode,
            'StopLoss': self._stopLoss,
            'StopLossPrice': self._stopLossPrice,
            'Threshold': self._threshold,
            'Status': 'Pending'
        }

    @property
    def stopLoss(self):
        return self._stopLoss

    @stopLoss.setter
    def stopLoss(self, val: int):
        self._stopLoss = val
        self.calcLoss()

    @property
    def stopLossPrice(self):
        return self._stopLossPrice

    @stopLossPrice.setter
    def stopLossPrice(self, val: float):
        self._stopLossPrice = val
        self.calcLoss(True)

    @property
    def loss(self):
        return self._loss

    def calcThresholdPrice(self):
        self._thresholdPrice = self._price * self._pos * self._threshold / 100.0

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, val: float):
        self._threshold = val
        self.calcThresholdPrice()

    @property
    def thresholdPrice(self):
        return self._thresholdPrice

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val: int):
        self._pos = val
        self.calcAllPrices()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, val: float):
        self._price = val
        self.calcAllPrices()
