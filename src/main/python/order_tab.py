from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget
from models.order_entry_model import OrderEntryModel
from ui.order_tab_ui import Ui_OrderTab
from models.main_model import mainModel


class OrderTab(QWidget, Ui_OrderTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mainModel = mainModel
        self.init_Ui()
        self.init_connection()

    def init_Ui(self):
        self._ui = Ui_OrderTab()
        self._ui.setupUi(self)

    def init_connection(self):
        self._ui.orderEntry.submitted.connect(self.on_order_entry_submitted)

    @pyqtSlot(OrderEntryModel)
    def on_order_entry_submitted(self, model: OrderEntryModel):
        trigger = {
            'ticker': model.ticker,
            'account': model.accounts[0] if len(model.accounts) else 'TEST',
            'sec_type': model.secType,
            'outside_rth': model.outsideRTH,
            'tif': model.tif,
            'order_type': model.orderType,
            'action': model.action,
            'entry_level': model.entryLevelData,
            'pt1': model.pt1Data,
            'pt2': model.pt2Data,
            'pt3': model.pt3Data,
            'pt4': model.pt4Data
        }
        id = self._mainModel.addTrigger(trigger)
        parentItem = self.insertTrigger2Table(id, trigger, 'entry_level')
        self.insertTrigger2Table(id, trigger, 'pt1', parentItem)
        self.insertTrigger2Table(id, trigger, 'pt2', parentItem)
        self.insertTrigger2Table(id, trigger, 'pt3', parentItem)
        self.insertTrigger2Table(id, trigger, 'pt4', parentItem)

    def insertTrigger2Table(self, id, trigger, level: str, parentItem: QTreeWidgetItem = None):
        data = trigger[level]
        item = QTreeWidgetItem(
            self._ui.trePendingOrders if parentItem is None else parentItem)
        item.setData(0, Qt.ItemDataRole.UserRole, id)
        item.setData(0, Qt.ItemDataRole.UserRole+1, level)
        item.setText(0, trigger['ticker'])
        item.setText(1, trigger['sec_type'])
        item.setText(2, trigger['action'])
        item.setText(3, trigger['account'])
        item.setText(
            4, trigger['tif'] + (" - outside RTH" if trigger['outside_rth'] else ""))
        item.setText(5, str(data['POS']))
        item.setText(6, trigger['order_type'] + " - " + str(data['Price']))
        item.setText(7, (str(data['StopLoss']) + " %") if not data['Mode']
                     == 'Fixed' else ("$ {}".format(data['StopLossPrice'])))
        item.setText(8, str(data['Threshold']) + " %")
        item.setText(9, data['Status'])
        if parentItem is None:
            self._ui.trePendingOrders.addTopLevelItem(item)
        return item
