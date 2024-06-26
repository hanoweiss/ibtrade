from datetime import datetime
from ib_insync import *
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

#ToDo: Scanner class
class OptionsTrader:
    #initialize Variables
    def __init__(self, *args, **kwargs):
        print("Options Trader Running, connecting to IB...")
        #connect to IB
        try:
            self.ib = IB()
            self.ib.connect(host='127.0.0.1', port=7496, clientId=1)
        except Exception as e:
                print(str(e))

        #Create SPY Contract
        self.underlying = Stock('SPY', 'SMART', 'USD')
        self.ib.qualifyContracts(self.underlying)

        print("Backfilling data to catchup...")

        #Request streaming bars
        self.data = self.ib.reqHistoricalData(self.underlying, endDateTime='', durationStr='2 D', barSizeSetting='1 min'
                                              , whatToShow='TRADES', useRTH=False, keepUpToDate=True,)

        #get current options chains
        self.chain = self.ib.reqSecDefOptParams(self.underlying.symbol, '', self.underlying.secType,
                                                self.underlying.conId)
        #update chain every hour
        update_chain_scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
        update_chain_scheduler.add_job(func=self.update_options_chains, trigger='cron', hour='*')
        update_chain_scheduler.start()

        print("Running Live")
        # Set callback function for streaming bars
        self.data.updateEvent += self.on_bar_update
        self.ib.execDetailsEvent += self.exec_status
        # Run forever

    # Update options chains
    def update_options_chains(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print("Updating options chains")
            # Get current options chains
            self.chains = self.ib.reqSecDefOptParams(self.underlying.symbol, '', self.underlying.secType,
                                                     self.underlying.conId)
            print(self.chains)
        except Exception as e:
            print(str(e))

    def on_bar_update(self, bars: BarDataList, has_new_bar: bool):
        #here i'll send the order command
        try:
            if has_new_bar:
                # Convert BarDataList to pandas Dataframe
                df = util.df(bars)
                # Check if we are in a trade
                if not self.in_trade:
                    print("Last Close : " + str(df.close.iloc[-1]))

                else:  # We are in a trade
                    print("AAA")
        except Exception as e:
            print(str(e))

        # Order Status
    def exec_status(self, trade: Trade, fill: Fill):
        print("Filled")

OT = OptionsTrader()
OT.on_bar_update(OT.data, True)