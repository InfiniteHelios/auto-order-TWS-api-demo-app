from logging import exception
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
import datetime
import traceback
import logging

from ui.main_window_ui import Ui_MainWindow
from service.ibapi_app import IBAPIApp


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connected = False

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        try:
            # self.ibapi_app = IBAPIApp()
            self.host = self.edtHost.text()
            self.port = int(self.edtPort.text())
            self.clientid = 123
            self.ibapi_app = IBAPIApp(self.host, self.port, self.clientid)
        except AttributeError:
            QMessageBox.critical(
                self,
                "Error",
                "IB API is not connected.\nPlease check the host and port valid.",
            )
