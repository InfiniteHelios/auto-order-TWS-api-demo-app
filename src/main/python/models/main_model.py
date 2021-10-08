from PyQt5.QtCore import QObject
from services.ibapi_app import IBapiApp


class MainModel(QObject):
    def __init__(self):
        super().__init__()
        self.host: str = '127.0.0.1'
        self.port: int = 7497
        self.client_id: int = 1
        self.app: IBapiApp = IBapiApp()

        self.accounts: list = []

    def __del__(self):
        try:
            self.app.disconnect()
        except:
            pass
        finally:
            del self.app


mainModel = MainModel()
