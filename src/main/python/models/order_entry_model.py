from PyQt5.QtCore import QObject
from models.main_model import mainModel


class OrderEntryModel(QObject):
    def __init__(self):
        super().__init__()
        self.app = mainModel.app

    def __del__(self):
        pass
