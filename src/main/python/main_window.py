from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot

from ui.main_window_ui import Ui_MainWindow
from service.ibapi_app import IBAPIApp

from ibapi.contract import Contract
import time


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connected = False

    def connect(self):
        try:
            # self.ibapi_app = IBAPIApp()
            self.host = self.edtHost.text()
            self.port = int(self.edtPort.text())
            self.clientid = int(self.edtClientId.text())
            self.ibapi_app = IBAPIApp(self.host, self.port, self.clientid)
            self.connected = True
            self.btnConnect.setText("Disconnect")
        except AttributeError:
            QMessageBox.critical(
                self,
                "Error",
                "IB API is not connected.\nPlease check the host and port valid.",
            )
    
    def disconnect(self):
        self.connected = False
        self.btnConnect.setText("Connect")
        self.ibapi_app.disconnect()

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        self.connect() if self.connected == False else self.disconnect()