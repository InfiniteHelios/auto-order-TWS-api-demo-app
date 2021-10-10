from PyQt5.QtCore import QObject
from models.main_model import mainModel


class OrderEntryModel(QObject):
    def __init__(self):
        super().__init__()
        self.app = mainModel.app

        self._levels = {
            'EntryLevel': {'POS': 100, 'Price': 10, 'Threshold': 3, 'Status': 'Pending'},
            'PT1': {'POS': 25, 'Price': 11, 'Threshold': 3, 'Status': 'Pending'},
            'PT2': {'POS': 25, 'Price': 12, 'Threshold': 3, 'Status': 'Pending'},
            'PT3': {'POS': 25, 'Price': 13, 'Threshold': 3, 'Status': 'Pending'},
            'PT4': {'POS': 25, 'Price': 14, 'Status': 'Pending'}
        }

    def __del__(self):
        pass

    @property
    def entryPos(self):
        return self._levels['EntryLevel']['POS']

    @entryPos.setter
    def entryPos(self, val: int):
        self._levels['EntryLevel']['POS'] = val
        pos = val
        val >>= 2
        self._levels['PT1']['POS'] = val
        pos = pos - val
        self._levels['PT2']['POS'] = val
        pos = pos - val
        self._levels['PT3']['POS'] = val
        pos = pos - val
        self._levels['PT4']['POS'] = pos

    @property
    def posPT1(self):
        return self._levels['PT1']['POS']

    @property
    def posPT2(self):
        return self._levels['PT2']['POS']

    @property
    def posPT3(self):
        return self._levels['PT3']['POS']

    @property
    def posPT4(self):
        return self._levels['PT4']['POS']

    @property
    def entryPrice(self):
        return self._levels['EntryLevel']['Price']

    @entryPrice.setter
    def entryPrice(self, val: float):
        self._levels['EntryLevel']['Price'] = val

    @property
    def entryStopLoss(self):
        return self._levels['EntryLevel']['StopLoss']

    @entryStopLoss.setter
    def entryStopLoss(self, val: int):
        self._levels['EntryLevel']['StopLoss'] = val
        self._levels['PT1']['StopLoss'] = val
        self._levels['PT2']['StopLoss'] = val
        self._levels['PT3']['StopLoss'] = val
        self._levels['PT4']['StopLoss'] = val

    @property
    def entryStopLossPrice(self):
        return self._levels['EntryLevel']['StopLossPrice']

    @entryStopLossPrice.setter
    def entryStopLossPrice(self, val: float):
        self._levels['EntryLevel']['StopLossPrice'] = val
        self._levels['PT1']['StopLossPrice'] = val
        self._levels['PT2']['StopLossPrice'] = val
        self._levels['PT3']['StopLossPrice'] = val
        self._levels['PT4']['StopLossPrice'] = val

    @property
    def entryLevelData(self):
        return self._levels['EntryLevel']

    @entryLevelData.setter
    def entryLevelData(self, val):
        self._levels['EntryLevel'] = val

    @property
    def pt1Data(self):
        return self._levels['PT1']

    @pt1Data.setter
    def pt1Data(self, val):
        self._levels['PT1'] = val

    @property
    def pt2Data(self):
        return self._levels['PT2']

    @pt2Data.setter
    def pt2Data(self, val):
        self._levels['PT2'] = val

    @property
    def pt3Data(self):
        return self._levels['PT3']

    @pt3Data.setter
    def pt3Data(self, val):
        self._levels['PT3'] = val

    @property
    def pt4Data(self):
        return self._levels['PT4']

    @pt4Data.setter
    def pt4Data(self, val):
        self._levels['PT4'] = val
