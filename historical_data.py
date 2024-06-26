
# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
import time


tickers = ["AAPL"]


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = pd.DataFrame([{"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low,
                                              "Close": bar.close, "Volume": bar.volume}])
        else:
            self.data[reqId] = pd.concat((self.data[reqId], pd.DataFrame([{"Date": bar.date, "Open": bar.open,
                                                                           "High": bar.high, "Low": bar.low,
                                                                           "Close": bar.close, "Volume": bar.volume}])))
            # self.data[reqId].append({"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume})
        print("reqID:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId, bar.date, bar.open,
                                                                                        bar.high, bar.low, bar.close,
                                                                                        bar.volume))

    def usTechStk(self, symbol, sec_type, strike, last_trade, right, order_id: int, currency="USD", exchange="SMART"):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange
        contract.currency = currency
        contract.lastTradeDateOrContractMonth = last_trade
        contract.strike = strike
        contract.right = right
        contract.multiplier = "100"
        self.reqMarketDataType(4)
        self.reqMktData(order_id, contract, "", 0, 0, [])
        return contract


def websocket_con():
    app.run()


app = TradeApp()
app.connect(host='127.0.0.1', port=7496,
            clientId=23)  # port 4002 for ib gateway paper trading/7497 for TWS paper trading
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established


###################storing trade app object in dataframe#######################
def dataDataframe(symbols, TradeApp_obj):
    "returns extracted historical data in dataframe format"
    df_data = {}
    for symbol in symbols:
        df_data[symbol] = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
        df_data[symbol].set_index("Date", inplace=True)
        # if you need to change the timezone of the candles, uncomment below line and change the time zones accordingly
        # df_data[symbol].index = pd.to_datetime(df_data[symbol].index, format='%Y%m%d %H:%M:%S %Z')
        # df_data[symbol].index= pd.DatetimeIndex(df_data[symbol].index).tz_convert("America/Indiana/Petersburg")
    return df_data



