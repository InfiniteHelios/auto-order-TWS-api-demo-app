import threading
import typing
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor
from models.main_model import MainModel
from ui.main_window_ui import Ui_MainWindow


class MainController(QObject):
    err_occured = pyqtSignal(str)
    con_err_occured = pyqtSignal()
    connected = pyqtSignal()
    disconnected = pyqtSignal()

    def __init__(self, model: MainModel, ui: Ui_MainWindow):
        super().__init__()
        self._model = model
        self._ui = ui
        # signal connection
        self._model.app.err_occured.connect(self.pushCriticalMsg)
        self._model.app.con_err_occured.connect(self.con_err_occured)
        self._model.app.connected.connect(self.on_connected)
        self._model.app.disconnected.connect(self.on_disconnected)

    def connect(self, host: str, port: int, client_id: int):
        self._model.host = host
        self._model.port = port
        self._model.client_id = client_id

        class ConnectorThread(QThread):
            finished = pyqtSignal(bool)

            def __init__(self, info: tuple, parent: typing.Optional[QObject] = ...) -> None:
                super().__init__(parent=parent)
                self._info = info

            def run(self):
                try:
                    self._info['app'].connect(
                        self._info['host'], self._info['port'], self._info['client_id'])
                except:
                    self.finished.emit(False)
                else:
                    self.finished.emit(True)

        thread = ConnectorThread(
            {
                'app': self._model.app,
                'host': self._model.host,
                'port': self._model.port,
                'client_id': self._model.client_id
            }, self)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self.on_connection_tried)
        thread.start()

    def disconnect(self):
        self._model.app.disconnect()

    @pyqtSlot(bool)
    def on_connection_tried(self, is_valid: bool):
        self.con_err_occured.emit() if not is_valid else None

    @pyqtSlot()
    def on_connected(self):
        self.connected.emit()
        threading.Thread(target=self._model.app.run, daemon=True).start()

    @pyqtSlot()
    def on_disconnected(self):
        self.disconnected.emit()

    @pyqtSlot(str)
    def pushSuccessMsg(self, msg: str):
        self._ui.txtConsole.moveCursor(
            QTextCursor.End, QTextCursor.MoveAnchor)
        self._ui.txtConsole.append("<p style='color: green;'>%s</p>" % msg)

    @pyqtSlot(str)
    def pushCriticalMsg(self, msg: str):
        self._ui.txtConsole.moveCursor(
            QTextCursor.End, QTextCursor.MoveAnchor)
        self._ui.txtConsole.append("<p style='color: red;'>%s</p>" % msg)
