from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSlot
from ibapi.contract import Contract
from ibapi.order import Order

from ui.order_entry_ui import Ui_OrderEntry
from service.ibapi_app import IBapiApp
from service.order_service import OrderService


class OrderEntry(QWidget, Ui_OrderEntry):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.cmbSecType.currentTextChanged.connect(self.on_cmbSecType_changed)

    def onServerConnected(self):
        """Called when TWS Api server is connected"""
        self.setEnabled(True)
        self.app = IBapiApp.app
        self.app.openOrderEndHandler = self.openOrderEndHandler
        self.app.managedAccountsHandler = self.managedAccountsHandler

    @pyqtSlot()
    def on_edtFinInstr_editingFinished(self):
        """Contract symbol edit is finished with the key ENTER or focous out"""
        if not self.app:
            return
        contract = self.contract()
        reqId = self.app.nextReqestId()
        self.app.reqMktData(reqId, contract, "", True, False, [])
        print("Last Price, ASK, MID, BID are requested.")

    def marketDataHandler(self):
        """Receive live market data and fill the last price"""
        self.spnLastPrice.setValue(0.08)

    @pyqtSlot()
    def on_radSell_toggled(self):
        if self.radSell.isChecked():
            self.setLayoutForSell()
        else:
            self.setLayoutForBuy()

    def setLayoutForSell(self):
        self.cmbOrderType.setEnalbed(False)
        self.cmbOrderType.setCurrentText("LMT")
        self.cmbTimeIF.setEnabled(False)
        self.cmbTimeIF.setCurrentText("GTC")
        self.chkOutsideRTH.setEnabled(False)
        self.chkOutsideRTH.setCheckState(Qt.CheckState.Unchecked)

    def setLayoutForBuy(self):
        self.cmbOrderType.setEnalbed(True)
        self.cmbTimeIF.setEnabled(True)
        self.chkOutsideRTH.setEnabled(True)
        self.chkOutsideRTH.setCheckState(Qt.CheckState.Checked)

    def on_cmbSecType_changed(self, secType):
        if secType == "Stock":
            self.setLayoutForStock()
        else:
            self.setLayoutForOption()

    def setLayoutForStock(self):
        self.spnStopLoss.setSuffix(" $")
        self.spnPT1.setSuffix(" $")
        self.spnPT2.setSuffix(" $")
        self.spnPT3.setSuffix(" $")
        self.spnPT4.setSuffix(" $")

    def setLayoutForOption(self):
        self.spnStopLoss.setSuffix(" %")
        self.spnPT1.setSuffix(" %")
        self.spnPT2.setSuffix(" %")
        self.spnPT3.setSuffix(" %")
        self.spnPT4.setSuffix(" %")

    @pyqtSlot()
    def on_btnSubmit_clicked(self):
        """Place order"""
        # if not IBapiApp.app.started:
        #     QMessageBox.critical(
        #         self,
        #         "Error",
        #         "Please connect to server.",
        #     )
        #     return
        # if not self.validationCheck():
        #     return
        orderTrigger = self.createOrderTrigger()
        self.insertOrderTrigger(orderTrigger)

    def contract(self):
        # create contract
        ticker = self.edtFinInstr.text()
        secType = self.cmbSecType.currentText()
        return OrderService.contract(ticker, secType)

    def createOrderTrigger(self):
        contract = self.contract()
        # create main order
        action = "BUY" if self.radBuy.isChecked() else "SELL"
        orderType = self.cmbOrderType.currentText()
        pos = self.spnPos.value()
        entryLevel = self.spnEntryLevel.value()
        account = self.cmbAccount.currentText()
        tif = self.cmbTimeIF.currentText()
        outsideRth = self.chkOutsideRTH.isChecked()
        # create sub orders
        stopLoss = self.spnStopLoss.value()
        stopLossPrice = entryLevel / 100 * \
            (100-stopLoss) if self.spnStopLoss.suffix() == " %" else stopLoss
        threshold = self.spnThreshold.value()
        thresholdPrice = entryLevel / 100 * \
            (100+threshold) if self.spnThreshold.suffix() == " %" else threshold
        pt1 = self.spnPT1.value()
        pt1Price = entryLevel / 100 * \
            (100+pt1) if self.spnPT1.suffix() == " %" else pt1
        pt2 = self.spnPT2.value()
        pt2Price = entryLevel / 100 * \
            (100+pt2) if self.spnPT2.suffix() == " %" else pt2
        pt3 = self.spnPT3.value()
        pt3Price = entryLevel / 100 * \
            (100+pt3) if self.spnPT3.suffix() == " %" else pt3
        pt4 = self.spnPT4.value()
        pt4Price = entryLevel / 100 * \
            (100+pt4) if self.spnPT4.suffix() == " %" else pt4
        orderTrigger = OrderService.createOrderTrigger(
            contract, account, action, orderType, entryLevel, tif, pos, outsideRth,
            stopLossPrice, thresholdPrice, pt1Price, pt2Price, pt3Price, pt4Price)
        return orderTrigger

    def validationCheck(self):
        """Validation check for placing order"""
        if not self.radBuy.isChecked() and not self.radSell.isChecked():
            QMessageBox.critical(
                self,
                "Error",
                "Please select action type as Buy or Sell.",
            )
            return False
        if not self.spnEntryLevel.value():
            QMessageBox.critical(
                self,
                "Error",
                "Please select valid level entry.",
            )
            return False
        return True

    def insertOrderTrigger(self, orderTrigger):
        contract: Contract = orderTrigger['contract']
        mainOrder: Order = orderTrigger['order']
        trigger = orderTrigger['trigger']
        # insert main order
        mainItem = QTreeWidgetItem(self.trePendingOrders)
        mainItem.setText(0, contract.symbol)
        mainItem.setText(1, contract.secType)
        mainItem.setText(2, mainOrder.action)
        mainItem.setText(3, mainOrder.orderType)
        mainItem.setText(4, str(trigger['EntryLevel']))
        mainItem.setText(5, str(mainOrder.totalQuantity))
        mainItem.setText(6, mainOrder.tif)
        mainItem.setText(7, "Pending")
        mainItem.setData(0, Qt.ItemDataRole.UserRole+1, trigger)
        # insert trigger item
        if trigger:
            # stop loss
            stopLossItem = QTreeWidgetItem(mainItem)
            stopLossItem.setText(2, "SELL")
            stopLossItem.setText(4, str(trigger['StopLoss']))
            stopLossItem.setText(5, str(mainOrder.totalQuantity))
            stopLossItem.setText(7, "Pending")
            # threshold
            thresholdItem = QTreeWidgetItem(mainItem)
            thresholdItem.setText(2, "Threshold")
            thresholdItem.setText(4, str(trigger['Threshold']))
            thresholdItem.setText(7, "Pending")
            # pt1
            pt1Item = QTreeWidgetItem(mainItem)
            pt1Item.setText(2, "SELL")
            pt1Item.setText(4, str(trigger['PT1']))
            pt1Item.setText(5, str(mainOrder.totalQuantity * 0.25))
            pt1Item.setText(7, "Pending")
            # pt2
            pt2Item = QTreeWidgetItem(mainItem)
            pt2Item.setText(2, "SELL")
            pt2Item.setText(4, str(trigger['PT2']))
            pt2Item.setText(5, str(mainOrder.totalQuantity * 0.25))
            pt2Item.setText(7, "Pending")
            # pt3
            pt3Item = QTreeWidgetItem(mainItem)
            pt3Item.setText(2, "SELL")
            pt3Item.setText(4, str(trigger['PT3']))
            pt3Item.setText(5, str(mainOrder.totalQuantity * 0.25))
            pt3Item.setText(7, "Pending")
            # pt4
            pt4Item = QTreeWidgetItem(mainItem)
            pt4Item.setText(2, "SELL")
            pt4Item.setText(4, str(trigger['PT4']))
            pt4Item.setText(5, str(mainOrder.totalQuantity * 0.25))
            pt4Item.setText(7, "Pending")
        self.trePendingOrders.addTopLevelItem(mainItem)

    def managedAccountsHandler(self):
        self.cmbAccount.clear()
        for account in self.app.accounts:
            self.cmbAccount.addItem(account)

    def openOrderEndHandler(self):
        """Receive orders sent to TWS"""
        for orderId in IBapiApp.app.permId2ord:
            order = IBapiApp.app.permId2ord[orderId]
            row = self.tblOrders.rowCount()
            self.tblOrders.insertRow(row)
            self.tblOrders.setItem(
                row, 0, QTableWidgetItem(order.contract.symbol))
            self.tblOrders.setItem(row, 1, QTableWidgetItem(order.action))
            self.tblOrders.setItem(row, 2, QTableWidgetItem(order.orderType))
            self.tblOrders.setItem(
                row,
                3,
                QTableWidgetItem("%s %.2f" %
                                 (order.orderType, order.lmtPrice)),
            )
            self.tblOrders.setItem(
                row, 4, QTableWidgetItem(str(order.totalQuantity)))
            self.tblOrders.setItem(
                row, 5, QTableWidgetItem("%.2f" % order.auxPrice))
