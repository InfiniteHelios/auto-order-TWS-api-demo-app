from PyQt5.QtCore import QObject


class OrderModel(QObject):
    def __init__(self):
        super().__init__()

    def __del__(self):
        pass
