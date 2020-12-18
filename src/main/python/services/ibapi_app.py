from PyQt5.QtCore import QObject, pyqtSignal
from ibapi.utils import iswrapper
from ibapi.common import *
from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class IBapiApp(QObject, EWrapper, EClient):
    err_occured = pyqtSignal(str)
    connected = pyqtSignal()
    con_err_occured = pyqtSignal()
    disconnected = pyqtSignal()
    accounts_loaded = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self._accounts: list = []

    @iswrapper
    def connectAck(self):
        super().connectAck()
        self.connected.emit()

    def disconnect(self):
        EClient.disconnect(self)

    @iswrapper
    def connectionClosed(self):
        self.disconnected.emit()
        super().connectionClosed()

    @iswrapper
    def error(self, id: int, errorCode: int, errorMsg: str):
        super().error(id, errorCode, errorMsg)
        if errorCode == 502:
            self.con_err_occured.emit()
        else:
            self.err_occured.emit("Ibapi Error %d: %s" % (errorCode, errorMsg))

    @iswrapper
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        self._accounts = accountsList.split(",")
        self.accounts_loaded.emit(self._accounts)
