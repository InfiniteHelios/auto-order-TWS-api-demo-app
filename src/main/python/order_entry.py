from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from ibapi.order import Order

from ui.order_entry_ui import Ui_OrderEntry
from service.ibapi_app import IBapiApp
from service.contract_samples import ContractSamples


class OrderEntry(QWidget, Ui_OrderEntry):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_btnSubmit_clicked(self):
        if not IBapiApp.app.started:
            QMessageBox.critical(
                self,
                "Error",
                "Please connect to server.",
            )
            return
        if not self.validationCheck():
            return
        self.placeOrder()

    def on_connected(self):
        IBapiApp.app.openOrderEndHandler = self.openOrderEndHandler

    def orderCreate(self):
        order = Order()
        order.action = "BUY" if self.radBuy.isChecked() else "SELL"
        order.orderType = self.cmbOrderType.currentText()
        order.totalQuantity = self.spnQty.value()
        order.lmtPrice = self.spnPrice.value()
        order.tif = self.cmbTimeIF.currentText()
        return order

    def placeOrder(self):
        contract = ContractSamples.New(self.edtFinInstr.text())
        order = self.orderCreate()
        order.usePriceMgmtAlgo = True
        IBapiApp.app.placeOrder(IBapiApp.app.nextOrderId(), contract, order)
        for ord in IBapiApp.app.permId2ord:
            print("%d %s" % (ord.orderId, ord.status))

    def validationCheck(self):
        if not self.radBuy.isChecked() and not self.radSell.isChecked():
            QMessageBox.critical(
                self,
                "Error",
                "Please select action type as Buy or Sell.",
            )
            return False
        if not self.spnPrice.value():
            QMessageBox.critical(
                self,
                "Error",
                "Please select valid price.",
            )
            return False
        return True

    def openOrderEndHandler(self):
        print(IBapiApp.app.permId2ord)
        # for (order, value) in IBapiApp.app.permId2ord:
        #     row = self.tblOrders.rowCount()
        #     self.tblOrders.insertRow(row)
        #     self.tblOrders.setItem(row, 0, QTableWidgetItem(order.contract.symbol))
