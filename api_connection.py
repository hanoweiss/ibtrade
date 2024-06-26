# -*- coding: utf-8 -*-
"""
basic app - api connection test
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error {} {} {}".format(reqId, errorCode, errorString))


app = TradingApp()
app.connect("127.0.0.1", 7496, clientId=1)
app.run()
