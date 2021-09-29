from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
import threading

from ui.main_window_ui import Ui_MainWindow
from service.ibapi_app import IBapiApp
from waitingspinnerwidget import QtWaitingSpinner


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # spinner
        self.spinner = QtWaitingSpinner(self)
        self.spinner.setRoundness(70.0)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(12)
        self.spinner.setLineLength(10)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(10)
        self.spinner.setRevolutionsPerSecond(1)
        self.spinner.setColor(QColor(200, 200, 200))

        self.host = "127.0.0.1"
        self.port = 7496
        self.clientid = 1
        IBapiApp.app = IBapiApp(self.consoleHandler)
        IBapiApp.app.connectedHandler = self.onConnectedHandler
        IBapiApp.app.connectionClosedHandler = self.onConnectionClosedHandler

    def closeEvent(self, event):
        super(QMainWindow, self).closeEvent(event)
        IBapiApp.app.disconnect()
        IBapiApp.app.started = False

    def consoleHandler(self, msg: str):
        self.txtConsole.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
        self.txtConsole.append("<p>%s</p>" % msg)

    def connect(self):
        self.host = self.edtHost.text()
        try:
            self.port = int(self.edtPort.text())
            self.clientid = int(self.edtClientId.text())
        except:
            QMessageBox.critical(
                self, "Error", "Please check connection setting is valid."
            )
            self.spinner.stop()
            self.centralWidget().setEnabled(True)
            return

        self.api_thread = ConnectorThread(
            self.host, self.port, self.clientid, self)
        self.api_thread.finished.connect(self.connectingFinished)
        self.api_thread.start()

    def connectingFinished(self, connected: bool):
        self.api_thread.deleteLater()
        if connected:
            return
        IBapiApp.app.disconnect()
        self.centralWidget().setEnabled(True)
        self.spinner.stop()
        QMessageBox.critical(self, "Error", "Can't connect to server.")

    def onConnectedHandler(self):
        self.spinner.stop()
        self.centralWidget().setEnabled(True)
        self.btnConnect.setText("Disconnect")
        print("Connected to Trader Workstation.")

        self.tabOrderEntry.onServerConnected()

    def onConnectionClosedHandler(self):
        self.btnConnect.setText("Connect")
        self.centralWidget().setEnabled(True)
        if self.spinner.isSpinning:
            self.spinner.stop()
        print("Connection is closed.")

    def disconnect(self):
        IBapiApp.app.disconnect()

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        print("btnConnect is clicked.")
        self.centralWidget().setEnabled(False)
        self.spinner.start()
        self.connect() if IBapiApp.app.started == False else self.disconnect()

    @pyqtSlot()
    def on_btnClearConsole_clicked(self):
        self.txtConsole.clear()


class ConnectorThread(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, host, port, clientid, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.clientid = clientid

    def run(self):
        try:
            IBapiApp.app.connect(self.host, self.port, self.clientid)
            if not IBapiApp.app.serverVersion():
                self.finished.emit(False)
            else:
                thread = threading.Thread(target=IBapiApp.app.run, daemon=True)
                thread.start()
                self.finished.emit(True)
        except:
            self.finished.emit(False)
