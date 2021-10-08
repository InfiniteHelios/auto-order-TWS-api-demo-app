from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot

from ui.main_window_ui import Ui_MainWindow
from models.main_model import mainModel
from controllers.main_controller import MainController
from waitingspinnerwidget import QtWaitingSpinner


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_Ui()
        self._model = mainModel
        self._controller = MainController(self._model, self._ui)

        self.init_connection()

    def closeEvent(self, event):
        super(QMainWindow, self).closeEvent(event)
        del self._spinner
        del self._controller
        del self._model
        del self._ui

    def init_Ui(self):
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.set_connected_Ui(False)
        self.init_spinner()

    def init_connection(self):
        self._controller.err_occured.connect(self.on_err_occured)
        self._controller.con_err_occured.connect(self.on_con_err_occured)
        self._controller.disconnected.connect(self.on_disconnected)
        self._controller.connected.connect(self.on_connected)

    def set_connected_Ui(self, isConnected: bool = True):
        self._ui.btnConnect.setVisible(not isConnected)
        self._ui.btnDisconnect.setVisible(isConnected)

    def init_spinner(self):
        self._spinner = QtWaitingSpinner(self)
        self._spinner.setRoundness(70.0)
        self._spinner.setMinimumTrailOpacity(15.0)
        self._spinner.setTrailFadePercentage(70.0)
        self._spinner.setNumberOfLines(12)
        self._spinner.setLineLength(10)
        self._spinner.setLineWidth(5)
        self._spinner.setInnerRadius(10)
        self._spinner.setRevolutionsPerSecond(1)
        self._spinner.setColor(QColor(200, 200, 200))

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        try:
            host = self._ui.edtHost.text()
            port = int(self._ui.edtPort.text())
            client_id = int(self._ui.edtClientId.text())
        except:
            self.on_err_occured("Please check connection setting is valid.")
            return
        self.centralWidget().setEnabled(False)
        self._spinner.start()
        self._controller.connect(host, port, client_id)

    @pyqtSlot()
    def on_btnDisconnect_clicked(self):
        self.centralWidget().setEnabled(False)
        self._spinner.start()
        self._controller.disconnect()

    @pyqtSlot()
    def on_btnClearConsole_clicked(self):
        self._ui.txtConsole.clear()

    @pyqtSlot(str)
    def on_err_occured(self, msg: str):
        self._spinner.stop()
        self.centralWidget().setEnabled(True)
        QMessageBox.critical(self, "Error", msg)

    @pyqtSlot()
    def on_con_err_occured(self):
        self.on_err_occured('Error is occured in socket connection.')

    @pyqtSlot()
    def on_connected(self):
        self._spinner.stop()
        self.centralWidget().setEnabled(True)
        self.set_connected_Ui()
        self._controller.pushSuccessMsg("Connected to API")

    @pyqtSlot()
    def on_disconnected(self):
        self._spinner.stop()
        self.centralWidget().setEnabled(True)
        self.set_connected_Ui(False)
        self._controller.pushCriticalMsg("Disconnected")
