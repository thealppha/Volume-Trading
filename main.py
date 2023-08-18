from datetime import datetime

from coin import Coin
from params import Params
from grid_search import GridSearch
from volume_analyzer import PriceCheck
from volume_analyzer import VolumeAnalyzer

if __name__ == "__main__":

    symbols = ["BTCUSDT", "SOLUSDT"]

    interval = "1m"

    best_params = Params.best_params
    param_ranges = Params.param_ranges

    startDate = datetime(2000, 1, 1)
    endDate = datetime(2023, 8, 1)

    analyze_flag = False
    grid_search_flag = False

    for symbol in symbols:
        coin = Coin(symbol, 300, 1200, startDate, endDate, interval)

        if analyze_flag:
            coin.load_data()

            volume_analyzer = VolumeAnalyzer(best_params['ma_up_plus_ratio'], best_params['price_check_time'], best_params['price_check_tresh'],
                                             best_params['init_highest_profit'], best_params['stop_limit'], PriceCheck.Check_Both)
            volume_analyzer.analyze(coin)
            volume_analyzer.plot()

        elif grid_search_flag:
            coin.load_data()
            search = GridSearch(coin, param_ranges, symbol, startDate, endDate, interval)
            search.grid_search()

        else:
            coin.save_data()
