import requests
import pandas as pd
from datetime import datetime


class Coin:
    date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, symbol, small_length, big_length, start_date, end_date, interval):

        self.symbol = symbol

        self.small_length = small_length
        self.big_length = big_length

        self.start_date = start_date
        self.end_date = end_date

        self.start_time = int(start_date.timestamp() * 1000)
        self.end_time = int(end_date.timestamp() * 1000)

        self.interval = interval

    def get_profit(self, exit_index, enter_index):
        return self.df['Close'][exit_index % len(self.df['Close'])] / self.df['Close'][enter_index]

    def save_data(self):
        self.get_info()
        self.calc_ma()
        self.save_csv()

    def get_info(self):
        base_url = "https://api.binance.com/api/v3/klines"

        data = []
        while self.start_time < self.end_time:
            params = {
                "symbol": self.symbol,
                "interval": self.interval,
                "limit": 1000,
                "startTime": self.start_time,
                "endTime": self.end_time
            }

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data_ = response.json()
                data.extend(data_)
                self.start_time = data_[-1][0] + 1
            else:
                print(f"Request failed with status code: {response.status_code}")
                break

        selected_data = [[datetime.fromtimestamp(float(candle[i]) / 1000) if i == 0 else float(candle[i]) for i in range(len(candle)) if i in [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]] for candle in data]
        self.df = pd.DataFrame(selected_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Quote_Volume', 'Trades', 'Taker_Base_Volume', 'Taker_Quote_Volume'])

    def calc_ma(self):
        for window in [self.small_length, self.big_length]:
            self.df[f"ma_{window}"] = self.df['Volume'].rolling(window=window).mean()

    def save_csv(self):
        self.df.to_csv(f"data/RawData/{self.symbol}_{self.interval}_{self.start_date.date()}_{self.end_date.date()}.csv", index=False)

    def load_data(self):
        self.df = pd.read_csv(f"data/RawData/{self.symbol}_{self.interval}_{self.start_date.date()}_{self.end_date.date()}.csv")
