from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
import threading

from ui.main_window_ui import Ui_MainWindow
from service.ibapi_app import IBapiApp


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.host = "127.0.0.1"
        self.port = 7496
        self.clientid = 1
        IBapiApp.app = IBapiApp(self.consoleHandler)

    def closeEvent(self, event):
        super(QMainWindow, self).closeEvent(event)
        IBapiApp.app.disconnect()
        IBapiApp.app.started = False

    def consoleHandler(self, msg: str):
        self.txtConsole.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
        self.txtConsole.append("<p>%s</p>" % msg)

    def connect(self):
        self.tabWidget.setEnabled(False)
        self.host = self.edtHost.text()
        try:
            self.port = int(self.edtPort.text())
            self.clientid = int(self.edtClientId.text())
        except:
            QMessageBox.critical(
                self, "Error", "Please check connection setting is valid."
            )
            return

        class ConnectorThread(QThread):
            finished = pyqtSignal(bool)

            def __init__(self, host, port, clientid, parent=None):
                super().__init__(parent)
                self.host = host
                self.port = port
                self.clientid = clientid

            def run(self):
                IBapiApp.app.connect(self.host, self.port, self.clientid)
                if not IBapiApp.app.serverVersion():
                    self.finished.emit(False)
                else:
                    thread = threading.Thread(target=IBapiApp.app.run, daemon=True)
                    thread.start()
                    self.finished.emit(True)

        self.api_thread = ConnectorThread(self.host, self.port, self.clientid, self)
        self.api_thread.finished.connect(self.connectResult)
        self.api_thread.finished.connect(self.api_thread.deleteLater)
        self.api_thread.start()

    def connectResult(self, connected: bool):
        self.tabWidget.setEnabled(True)
        if not connected:
            QMessageBox.critical(self, "Error", "Can't connect to server.")
            return

        self.btnConnect.setText("Disconnect")

        self.tabOrderEntry.onServerConnected()

    def disconnect(self):
        IBapiApp.app.disconnect()
        IBapiApp.app.started = False
        self.btnConnect.setText("Connect")

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        self.connect() if IBapiApp.app.started == False else self.disconnect()

    @pyqtSlot()
    def on_btnClearConsole_clicked(self):
        self.txtConsole.clear()
