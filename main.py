import os
import pandas as pd

from datetime import datetime

from coin import Coin
from params import Params
from grid_search import GridSearch
from volume_analyzer import PriceCheck
from volume_analyzer import VolumeAnalyzer

if __name__ == "__main__":
    ###################### CHANGEABLE ######################
    analyze_flag = False
    grid_search_flag = True
    get_and_save_data_flag = False

    symbol = "SOLUSDT"
    limit_time = False
    ########################################################
    interval = "1m"

    best_params = Params.best_params
    param_ranges = Params.param_ranges

    if analyze_flag or grid_search_flag:
        # this if state for auto selection of exist csv file
        rawfiles = os.listdir("data/RawData")
        filename_will_be_analyzed = [i for i in rawfiles if i.startswith(symbol)][0]
        first_y, first_m, first_d = filename_will_be_analyzed.split("_")[2].split("-")
        last_y, last_m, last_d = filename_will_be_analyzed.split("_")[3].split(".")[0].split("-")

        startDate = datetime(int(first_y), int(first_m), int(first_d))
        endDate = datetime(int(last_y), int(last_m), int(last_d))
    else:
        # this is for fetching data
        ###################### CHANGEABLE ######################
        startDate = datetime(2017, 8, 21)
        endDate = datetime(2023, 8, 18)
        ########################################################

    coin = Coin(symbol, 300, 1200, startDate, endDate, interval)

    if analyze_flag or grid_search_flag:
        coin.load_data()

        if limit_time:
            # Times which be wanted to analyze
            ###################### CHANGEABLE ######################
            analyze_start_date = datetime(2019, 8, 1)
            analyze_end_date = datetime(2019, 8, 30)
            ########################################################

            coin.df = coin.df[(pd.to_datetime(coin.df["Date"]) > analyze_start_date) & (pd.to_datetime(coin.df["Date"]) < analyze_end_date)]
            coin.df.reset_index(drop=True, inplace=True)

        if analyze_flag:
            volume_analyzer = VolumeAnalyzer(best_params['ma_up_plus_ratio'], best_params['price_check_time'], best_params['price_check_tresh'],
                                             best_params['init_highest_profit'], best_params['stop_limit'], PriceCheck.Check_Both)
            volume_analyzer.analyze(coin)
            volume_analyzer.plot()

        elif grid_search_flag:

            search = GridSearch(coin, param_ranges, symbol, startDate, endDate, interval)
            search.grid_search()

    else:
        coin.get_and_save_data()
