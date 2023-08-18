import pandas as pd

from itertools import product
from volume_analyzer import PriceCheck
from volume_analyzer import VolumeAnalyzer


class GridSearch:
    df_iteratives = pd.DataFrame(columns=['ma_up_plus_ratio', 'price_check_time', 'price_check_tresh',
                                          'init_highest_profit', 'stop_limit', 'profit'])

    def __init__(self, coin, param_ranges, symbol, start_date, end_date, interval):
        self.coin = coin
        self.param_ranges = param_ranges
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval

    def grid_search(self):
        best_profit = float('-inf')  # Assuming you're maximizing a profit

        # Generate all parameter combinations
        param_combinations = product(*self.param_ranges.values())

        # Find the length of param_combinations
        num_combinations = len(list(param_combinations))

        # Loop through each combination
        for ind, combination in enumerate(param_combinations):
            param_dict = dict(zip(self.param_ranges.keys(), combination))

            combination_params = [param_dict['ma_up_plus_ratio'], param_dict['price_check_time'], param_dict['price_check_tresh'],
                                  param_dict['init_highest_profit'], param_dict['stop_limit'], PriceCheck.Check_Both]

            volume_analyzer = VolumeAnalyzer(*combination_params)

            current_profit = volume_analyzer.analyze(self.coin)

            GridSearch.df_iteratives.loc[ind] = combination_params[:-1] + [current_profit]

            # Check if current combination is better than previous best
            if current_profit > best_profit:
                best_profit = current_profit

            print(f"Grid Search Index : {ind+1} | Completion Percentage : % {100 * (ind+1) / num_combinations}\n")

            GridSearch.df_iteratives.to_csv(f"data/GridSearch/GridSearch_Iteratives_{self.symbol}_{self.interval}_{self.start_date.date()}_{self.end_date.date()}.csv", index=False)

        sorted_df = GridSearch.df_iteratives.sort_values(by="profit", ascending=False)
        best_combinations = sorted_df[sorted_df["profit"] == sorted_df["profit"].max()]

        best_combinations.to_csv(f"data/GridSearch/GridSearch_Best_Combinations_{self.symbol}_{self.interval}_{self.start_date.date()}_{self.end_date.date()}.csv", index=False)