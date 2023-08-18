import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

from enum import Enum


class PriceChange(Enum):
    No_Change = 0
    Long = 1
    Short = 2


class PriceCheck(Enum):
    No_Check = 0
    Check_Long = 1
    Check_Short = 2
    Check_Both = 3


price_change_2_price_check_funcs = {
    PriceCheck.No_Check: lambda price_change: True,
    PriceCheck.Check_Long: lambda price_change: price_change == PriceChange.Long,
    PriceCheck.Check_Short: lambda price_change: price_change == PriceChange.Short,
    PriceCheck.Check_Both: lambda price_change: price_change != PriceChange.No_Change
}


class VolumeAnalyzer:
    def __init__(self, ma_up_plus_ratio, price_check_time, price_check_tresh, init_highest_profit, stop_limit, price_change):
        self.ma_up_plus_ratio = ma_up_plus_ratio
        self.price_check_time = price_check_time
        self.price_check_tresh = price_check_tresh
        self.init_highest_profit = init_highest_profit
        self.stop_limit = stop_limit
        self.price_check_func = price_change_2_price_check_funcs.get(price_change)

    def analyze(self, coin):

        def get_price_change(past_profit):
            if abs(past_profit - 1) < self.price_check_tresh:
                price_change = PriceChange.No_Change
            else:
                price_change = PriceChange.Long if past_profit > 1 else PriceChange.Short
            return price_change

        # 5, 20 den büyük
        coin.df['ma_up'] = coin.df['ma_300'] > coin.df['ma_1200']

        # 5, 20 nin 1.2 katından büyük
        coin.df['ma_up_plus'] = coin.df['ma_300'] > (self.ma_up_plus_ratio * coin.df['ma_1200'])

        # tüm indexler
        ma_up_indexes = coin.df[coin.df['ma_up_plus'] == True].index

        enter_indexes = []
        exit_indexes = []

        profits = []
        # coin.df["profits"] = 1

        for index in ma_up_indexes:
            if len(exit_indexes) != 0:
                if exit_indexes[-1] > index:
                    continue

            past_profit = coin.get_profit(index, index - self.price_check_time)
            price_change = get_price_change(past_profit)

            if self.price_check_func(price_change):

                highest_profit = self.init_highest_profit
                profit = 1
                enter_index = index
                enter_indexes.append(enter_index)

                while profit > (1 - self.stop_limit) * highest_profit:
                    if len(coin.df) - 1 == index:
                        break
                    else:
                        index += 1

                    profit = coin.get_profit(index, enter_index)

                    if price_change == PriceChange.Short:
                        profit = 1 / profit

                    if profit > highest_profit:
                        highest_profit = profit

                exit_index = index
                exit_indexes.append(exit_index)

                # coin.df["profits"].iloc[exit_index] = profit
                profits.append(profit)

                # print("index     ", coin.df["Date"][enter_index], price_change.name, coin.df["Date"][exit_index], enter_index, exit_index, profit, get_price_change(profit).name)
            else:
                pass
                # print("index     ", coin.df["Date"][index], price_change.name)

        # coin.df.to_csv(f"data/Final_{symbol}_{interval}_{startDate.date()}_{endDate.date()}.csv", index=False)

        print(f"{coin.symbol} PARAMS | Stop Limit: {self.stop_limit} "
              f"| Price Comparison Time: {self.price_check_time} "
              f"| Price Comparison Ratio: {self.price_check_tresh} "
              f"| MA Comparison Ratio: {self.ma_up_plus_ratio} "
              f"| Trade Number: {len(exit_indexes)} "
              f"| Default Profit: {round(coin.get_profit(-1, 0), 2)} "
              f"| Our Profit: {round(np.prod(profits), 2)}")

        return round(np.prod(profits), 2)

    def plot(self):
        pass
        # fig, ax1 = plt.subplots(figsize=(18, 8))
        #
        # self.coin.df['Date'] = self.coin.df.index
        # self.coin.df.index = pd.DatetimeIndex(self.coin.df['Date'])
        #
        # mpf.plot(self.coin.df, type='candle', ax=ax1, style='binance', show_nontrading=True)
        # x_interval = 3
        # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d  %H:%M'))
        # ax1.xaxis.set_major_locator(mdates.HourLocator(interval=x_interval))
        # ax1.tick_params(axis='x', rotation=90)
        #
        # for i in range(len(self.coin.df['ma_up'])):
        #     if self.coin.df['ma_up'][i]:
        #         ax1.scatter(self.coin.df.index[i], self.coin.df['Close'][i], color='green', marker='o')
        #
        # ax1.grid(True)
        #
        # colors = ['blue', 'red', 'orange']
        # scale = 2.0
        #
        # fig2, (ax2, ax3) = plt.subplots(nrows=4, figsize=(18, 8), sharex=True)
        # tick_locs = ax2.get_xticks()
        # bar_width = 0.8 * (tick_locs[1] - tick_locs[0]) / x_interval
        #
        # ax2.plot(self.coin.df.index, self.coin.df['ma_5'], color=colors[0], linewidth=2)
        # ax2.plot(self.coin.df.index, self.coin.df['ma_20'], color=colors[1], linewidth=2)
        # ax2.set_ylim(0, self.coin.df['ma_5'].max() * scale)
        # ax2.grid(True)
        #
        # ax_std = ax2.twinx()
        # ax_std.plot(self.coin.df.index, self.coin.df['ma_up'], color=colors[2], linewidth=2)
        # ax_std.set_ylim(-1, 1.1)
        # ax_std.spines['right'].set_position(('outward', 10))
        # ax_std.set_ylabel('ma_up')
        # ax_std.spines['right'].set_visible(True)
        # ax_std.spines['right'].set_color(colors[2])
        #
        # ax3.bar(self.coin.df.index, self.coin.df['Volume'], color=colors[0], width=bar_width)
        # ax3.bar(self.coin.df.index, self.coin.df['Taker_Base_Volume'], color=colors[1], width=bar_width)
        # ax3.set_ylim(0, self.coin.df['Volume'].max() * scale)
        # ax3.grid(True)
        #
        # legend_elements = [Line2D([0], [0], color=colors[0], linewidth=2, label='ma_5'),
        #                    Line2D([0], [0], color=colors[1], linewidth=2, label='ma_20')]
        #
        # ax2.legend(handles=legend_elements, loc='upper left')
        #
        # plt.show()
