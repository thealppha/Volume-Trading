import numpy as np


class Params:
    param_ranges = {
        'ma_up_plus_ratio': np.arange(1.6, 2.4, 0.2).round(2),
        'price_check_time': [15, 30, 60],
        'price_check_tresh': np.arange(0.001, 0.007, 0.001).round(3),
        'init_highest_profit': np.arange(1, 2, 0.1).round(2),
        'stop_limit': np.arange(0.05, 0.11, 0.01).round(2)
    }

    # TODO
    #  GridSearch flag aktif değilken,
    #  belirlemiş olduğumuz best parametreler burada atanacaktır ve
    #  gridsearch yapmadan sadece volume analyze de kullanılacaktır
    best_params = {
        'ma_up_plus_ratio': 2,
        'price_check_time': 30,
        'price_check_tresh': 0.004,
        'init_highest_profit': 1.05,
        'stop_limit': 0.1
    }
