from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QGroupBox
from controllers.order_entry_level_controller import OrderEntryLevelController
from models.order_entry_level_model import OrderEntryLevelModel
from ui.order_entry_level_ui import Ui_OrderEntryLevel
from ui.order_entry_ui import Ui_OrderEntry


class OrderEntryLevel(QGroupBox, Ui_OrderEntryLevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_Ui()

        self._model = OrderEntryLevelModel(self._ui)
        self._controller = OrderEntryLevelController(self._model, self._ui)
        self._parent_ui: Ui_OrderEntry = parent._ui

        self.init_connection()
        self.clear_Ui()

    def __del__(self):
        del self._controller
        del self._model

    def init_Ui(self):
        self._ui = Ui_OrderEntryLevel()
        self._ui.setupUi(self)
        # self.setEnabled(False)
        self.setStockLayout()

    def init_connection(self):
        self._parent_ui.cmbSecType.currentTextChanged.connect(
            self.on_type_changed)

    def clear_Ui(self):
        self.setPercentModeLayout()

    @pyqtSlot(str)
    def on_type_changed(self, type: str):
        self.setStockLayout() if type == 'Stock' else self.setOptionLayout()
        self.on_cmbStopLoss_currentIndexChanged(
            self._ui.cmbStopLoss.currentIndex())

    def setStockLayout(self):
        self._ui.cmbStopLoss.blockSignals(True)
        self._ui.cmbStopLoss.clear()
        items = ["3 %", "4 %", "5 %", "6 %", "7 %", "8 %"]
        data = [3, 4, 5, 6, 7, 8]
        self._ui.cmbStopLoss.addItems(items)
        for (x, i) in enumerate(data):
            self._ui.cmbStopLoss.setItemData(x, i)
        self._ui.cmbStopLoss.blockSignals(False)

    def setOptionLayout(self):
        self._ui.cmbStopLoss.blockSignals(True)
        self._ui.cmbStopLoss.clear()
        items = ["10 %", "12 %", "14 %", "16 %", "18 %", "20 %"]
        data = [10, 12, 14, 16, 18, 20]
        self._ui.cmbStopLoss.addItems(items)
        for (x, i) in enumerate(data):
            self._ui.cmbStopLoss.setItemData(x, i)
        self._ui.cmbStopLoss.blockSignals(False)

    @pyqtSlot(bool)
    def on_radFixedPrice_toggled(self, checked: bool):
        self.setPercentModeLayout() if not checked else self.setFixedModeLayout()

    def setPercentModeLayout(self):
        self._ui.spnStopLossPrice.setVisible(False)
        self._ui.cmbStopLoss.setVisible(True)
        self._controller.stopLossUpdated(self._model.stopLoss)

    def setFixedModeLayout(self):
        self._ui.spnStopLossPrice.setVisible(True)
        self._ui.cmbStopLoss.setVisible(False)
        self._controller.stopLossPriceUpdated(self._model.stopLossPrice)

    @pyqtSlot(int)
    def on_cmbStopLoss_currentIndexChanged(self, cur: int):
        data = self._ui.cmbStopLoss.itemData(cur, Qt.ItemDataRole.UserRole)
        self._controller.stopLossUpdated(data)

    @pyqtSlot(float)
    def on_spnStopLossPrice_valueChanged(self, val: float):
        self._controller.stopLossPriceUpdated(val)

    @pyqtSlot(float)
    def on_spnThreshold_valueChanged(self, val: float):
        self._controller.thresholdUpdated(val)

    @pyqtSlot(int)
    def on_spnPos_valueChanged(self, val: int):
        self._controller.posUpdated(val)

    @pyqtSlot(float)
    def on_spnPrice_valueChanged(self, val: float):
        self._controller.priceUpdated(val)

    def setPos(self, val: int, max: int = -1, min: int = 0):
        self._ui.spnPos.setValue(val)
        self._ui.spnPos.setMinimum(min)
        if max > 0:
            self._ui.spnPos.setMaximum(max)

    def hideThreshold(self):
        self._ui.spnThreshold.setVisible(False)
        self._ui.spnThresholdPrice.setVisible(False)
        self._ui.labForThreshold.setVisible(False)
