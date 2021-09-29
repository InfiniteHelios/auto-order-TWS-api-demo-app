from ibapi.contract import Contract
from ibapi.order import Order
from service.contract_samples import ContractSamples
from service.order_samples import OrderSamples


class OrderService:

    @staticmethod
    def createOrderTrigger(contract: Contract, account: str, action: str,
                           orderType: str, entryLevel,  tif: str, pos=100, outsideRTH=True,
                           stopLossPrice=None, thresholdPrice=None,
                           pt1Price=None, pt2Price=None, pt3Price=None, pt4Price=None):
        mainOrder = OrderService.mainOrder(
            action, orderType, pos, entryLevel, account, tif, outsideRTH)
        trigger = OrderService.orderTrigger(
            mainOrder, entryLevel, stopLossPrice, thresholdPrice, pt1Price, pt2Price, pt3Price, pt4Price)
        result = {}
        result['contract'] = contract
        result['order'] = mainOrder
        result['trigger'] = trigger
        return result

    @staticmethod
    def contract(symbol: str, secType: str = "STK"):
        contract = ContractSamples.New(symbol)
        contract.secType = secType
        return contract

    @staticmethod
    def mainOrder(action: str, orderType: str, pos, entryLevel, account: str, tif: str, outsideRTH=True):
        if orderType == "LMT":
            order = OrderSamples.LimitOrder(action, pos, entryLevel)
        elif orderType == "MKT":
            order = OrderSamples.MarketOrder(action, pos, entryLevel)
        elif orderType == "MID":
            order = OrderSamples.Midprice(action, pos, entryLevel)

        order.account = account
        order.tif = tif
        order.outsideRth = outsideRTH
        order.usePriceMgmtAlgo = True
        return order

    @staticmethod
    def orderTrigger(order: Order, entryLevel, stopLossPrice, thresholdPrice, pt1Price, pt2Price, pt3Price, pt4Price):
        if entryLevel == stopLossPrice or stopLossPrice == 0:
            return None
        result = {}
        result['EntryLevel'] = entryLevel
        result['Pos'] = order.totalQuantity
        result['RestPos'] = order.totalQuantity
        result['StopLoss'] = stopLossPrice
        result['Threshold'] = thresholdPrice
        result['PT1'] = pt1Price
        result['PT2'] = pt2Price
        result['PT3'] = pt3Price
        result['PT4'] = pt4Price
        return result
