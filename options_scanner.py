from yahoo_fin import options
import yfinance as yf
import pandas as pd


class OptionScanner:
    def __init__(self):
        self.options_df = pd.DataFrame()

# create a data frame:
    def create_scanner_dataframe(self, df, stock, is_positive_return, net_income, yearly_return):
        new_data = {
            "Stock": [stock],
            "Net Income": [is_positive_return],
            "Yearly Return": [net_income],
            "Yearly Return > 7%": [yearly_return]
        }

        new_df = pd.DataFrame(new_data)
        # Append the new data to the existing DataFrame
        self.options_df = pd.concat([df, new_df], ignore_index=True)

    def find_closest_lower_number(self, list, number):
        for num in list:
            if num > number:
                return current
            else:
                current = num
                continue

    def calculate_yield(self, date, deal_income, call_mid, put_mid, current_price):
        dte = (pd.Timestamp(date) - pd.Timestamp('today')).days
        yearly_multiplier = 360/dte
        return (deal_income/((current_price + put_mid - call_mid)*100)) * yearly_multiplier

    def calculate_deal_condition(self, stock, date, strike, current_price, commission):
        stock = stock
        date = date
        current_price = current_price
        strike = strike

        pd.set_option('display.max_columns', None)

        calls = options.get_calls(stock, date)
        puts = options.get_puts(stock, date)

        call = calls[calls['Strike'] == strike]
        call_mid_price = (call['Bid'].values[0] + call['Ask'].values[0])/2

        put = puts[puts['Strike'] == strike]
        put_mid_price = (put['Bid'].values[0] + put['Ask'].values[0])/2

        deal_income = (call_mid_price + strike)*100 - (current_price + put_mid_price)*100 - commission
        yearly_yield = self.calculate_yield(date, deal_income, call_mid_price, put_mid_price, current_price)
        return stock, deal_income, yearly_yield*100, yearly_yield*100 > 7

    def calculate_number_of_valid_deals(self):
        row_counter = 0
        valid_deals_counter = 0
        for row in self.options_df.iterrows():
            if list(row)[1][3]:
                valid_deals_counter += 1
                row_counter += 1
            else:
                row_counter += 1
        return valid_deals_counter, (valid_deals_counter/row_counter) * 100

    def create_tickers_list(self, date):
        ticker_list = []
        tickers = pd.read_html(
            'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].Symbol.array
        #check if option chain exists
        for ticker in tickers:
            try:
                calls = options.get_calls(ticker, date)
                ticker_list.append(ticker)
            except:
                pass
        return tickers


# script inputs
date = 'December 08, 2023'
OS = OptionScanner()
tickers = OS.create_tickers_list(date)
#tickers = ['AAPL', 'WBD', 'QS', 'PARA']
for ticker in tickers:
    stock = ticker
    stock_data = yf.Ticker(stock)
    current_price = stock_data.basic_info.last_price
    commission = 3.02
    try:
        strikes = options.get_calls(stock, date).Strike.array
    except:
        continue
    strike = OS.find_closest_lower_number(strikes, current_price)
    a = OS.calculate_deal_condition(stock, date, strike, current_price, commission)

    OS.create_scanner_dataframe(OS.options_df, a[0], a[1], a[2], a[3])

scanner_stats = OS.calculate_number_of_valid_deals()
a = 5

