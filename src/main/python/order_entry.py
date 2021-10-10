import PyQt5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QWidget
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
        self.clear_Ui()

    def __del__(self):
        del self._controller
        del self._model

    def init_Ui(self):
        self._ui = Ui_OrderEntry()
        self._ui.setupUi(self)
        # self.setEnabled(False)

    def init_connection(self):
        self._ui.groupEntryLevel._ui.spnPos.valueChanged.connect(
            self.on_entryPos_changed)
        self._ui.groupEntryLevel._ui.spnPrice.valueChanged.connect(
            self.on_entryPrice_changed)
        self._ui.groupEntryLevel._ui.cmbStopLoss.currentIndexChanged.connect(
            self.on_entryStopLossIndex_changed)
        self._ui.groupEntryLevel._ui.spnThreshold.valueChanged.connect(
            self.on_entryThreshold_changed)
        self._ui.groupEntryLevel._ui.radFixedPrice.toggled.connect(
            self.on_entryMode_changed)
        self._ui.groupEntryLevel._ui.spnStopLossPrice.valueChanged.connect(
            self.on_entryStopLossPrice_changed)
        self._ui.btnSubmit.clicked.connect(self.on_submit)

    def clear_Ui(self):
        self._ui.groupPT4.hideThreshold()
        self.on_entryPos_changed(self._model.entryPos)
        self.on_entryPrice_changed(self._model.entryPrice)

    @pyqtSlot(int)
    def on_entryPos_changed(self, val: int):
        self._model.entryPos = val
        self._ui.groupPT1.setPos(self._model.posPT1, max=val)
        self._ui.groupPT2.setPos(self._model.posPT2, max=val)
        self._ui.groupPT3.setPos(self._model.posPT3, max=val)
        self._ui.groupPT4.setPos(self._model.posPT4, max=val)

    @pyqtSlot(float)
    def on_entryPrice_changed(self, val: float):
        self._model.entryPrice = val
        self._ui.groupPT1._ui.spnPrice.setMinimum(val)
        self._ui.groupPT2._ui.spnPrice.setMinimum(val)
        self._ui.groupPT3._ui.spnPrice.setMinimum(val)
        self._ui.groupPT4._ui.spnPrice.setMinimum(val)

    @pyqtSlot(int)
    def on_entryStopLossIndex_changed(self, index: int):
        self._ui.groupEntryLevel._ui.spnPrice.blockSignals(True)
        self._ui.groupPT1._ui.cmbStopLoss.setCurrentIndex(index)
        self._ui.groupPT2._ui.cmbStopLoss.setCurrentIndex(index)
        self._ui.groupPT3._ui.cmbStopLoss.setCurrentIndex(index)
        self._ui.groupPT4._ui.cmbStopLoss.setCurrentIndex(index)
        self._ui.groupEntryLevel._ui.spnPrice.blockSignals(False)

    @pyqtSlot(float)
    def on_entryThreshold_changed(self, val: float):
        self._ui.groupPT1._ui.spnThreshold.setValue(val)
        self._ui.groupPT2._ui.spnThreshold.setValue(val)
        self._ui.groupPT3._ui.spnThreshold.setValue(val)

    @pyqtSlot(bool)
    def on_entryMode_changed(self, isFixedMode: bool):
        self._ui.groupPT1._ui.radFixedPrice.setChecked(
            True) if isFixedMode else self._ui.groupPT1._ui.radPercentage.setChecked(True)
        self._ui.groupPT2._ui.radFixedPrice.setChecked(
            True) if isFixedMode else self._ui.groupPT2._ui.radPercentage.setChecked(True)
        self._ui.groupPT3._ui.radFixedPrice.setChecked(
            True) if isFixedMode else self._ui.groupPT3._ui.radPercentage.setChecked(True)
        self._ui.groupPT4._ui.radFixedPrice.setChecked(
            True) if isFixedMode else self._ui.groupPT4._ui.radPercentage.setChecked(True)

    @pyqtSlot(float)
    def on_entryStopLossPrice_changed(self, val: float):
        self._ui.groupPT1._ui.spnStopLossPrice.setValue(val)
        self._ui.groupPT2._ui.spnStopLossPrice.setValue(val)
        self._ui.groupPT3._ui.spnStopLossPrice.setValue(val)
        self._ui.groupPT4._ui.spnStopLossPrice.setValue(val)

    @pyqtSlot()
    def on_submit(self):
        # get selected accounts
        accounts = self.selectedAccounts()
        if len(accounts) == 0:
            QMessageBox.warning(
                self, "Warning", "Please select more than one account.")
            return
        self._controller.submit(accounts)

    def selectedAccounts(self):
        result = []
        for i in range(self._ui.layTicker.count()):
            item = self._ui.layTicker.itemAt(i).widget()
            if item.__class__ == QCheckBox and item.isChecked():
                result.append(item.text())
        return result

    def set_disconnected_Ui(self):
        for i in range(self._ui.layTicker.count()):
            item = self._ui.layTicker.itemAt(i).widget()
            if item.__class__ == QCheckBox:
                item.deleteLater()
