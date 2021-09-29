from ibapi import ticktype
from ibapi.order_condition import ExecutionCondition
from ibapi.utils import iswrapper
from ibapi.common import *
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class IBapiApp(EWrapper, EClient):
    app = None

    def __init__(self, errorHandler=None):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        self.started = False
        self.nextValidOrderId = None
        self.nextReqId = 1
        self.permId2ord = {}
        self.accounts = []

        # handlers
        self.errorHandler = errorHandler
        self.connectedHandler = None
        self.connectionClosedHandler = None
        self.openOrderEndHandler = None
        self.managedAccountsHandler = None

    def isConnected(self):
        prev = self.started
        self.started = super().isConnected()
        if self.connectedHandler and not prev and self.started:
            self.connectedHandler()
        return self.started

    @iswrapper
    def connectionClosed(self):
        if self.connectionClosedHandler:
            self.connectionClosedHandler()
        self.started = False
        return super().connectionClosed()

    @iswrapper
    def connectAck(self):
        if self.asynchronous:
            self.startApi()

    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        self.start()

    def start(self):
        if self.started:
            return

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def nextReqestId(self):
        oid = self.nextReqId
        self.nextReqId += 1
        return oid

    @iswrapper
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        msg = "Error.Id: %d Code %d Msg: %s" % (reqId, errorCode, errorString)
        print(msg) if not self.errorHandler else self.errorHandler(msg)

    @iswrapper
    def winError(self, text: str, lastError: int):
        super().winError(text, lastError)
        msg = "Error.Code %d Msg: %s" % (lastError, text)
        print(msg) if not self.errorHandler else self.errorHandler(msg)

    @iswrapper
    def currentTime(self, time: int):
        super().currentTime(time)

    @iswrapper
    def openOrder(
        self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState
    ):
        super().openOrder(orderId, contract, order, orderState)
        order.contract = contract
        self.permId2ord[order.permId] = order

    @iswrapper
    def openOrderEnd(self):
        super().openOrderEnd()
        self.openOrderEndHandler() if self.openOrderEndHandler else print(
            "Received %d openOrders", len(self.permId2ord)
        )

    @iswrapper
    def orderStatus(
        self,
        orderId: OrderId,
        status: str,
        filled: float,
        remaining: float,
        avgFillPrice: float,
        permId: int,
        parentId: int,
        lastFillPrice: float,
        clientId: int,
        whyHeld: str,
        mktCapPrice: float,
    ):
        super().orderStatus(
            orderId,
            status,
            filled,
            remaining,
            avgFillPrice,
            permId,
            parentId,
            lastFillPrice,
            clientId,
            whyHeld,
            mktCapPrice,
        )

    @iswrapper
    def execDetails(
        self, reqId: int, contract: Contract, execution: ExecutionCondition
    ):
        super().execDetails(reqId, contract, execution)

    @iswrapper
    def orderBound(self, orderId: int, apiClientId: int, apiOrderId: int):
        super().orderBound(orderId, apiClientId, apiOrderId)

    @iswrapper
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        self.accounts = accountsList.split(",")
        if self.managedAccountsHandler:
            self.managedAccountsHandler()

    def tickPrice(
        self, reqId: TickerId, tickType: ticktype, price: float, attrib: TickAttrib
    ):
        super().tickPrice(reqId, tickType, price, attrib)
        print("ReqId: %d tickType: %d price: %d" % (reqId, tickType, price))
