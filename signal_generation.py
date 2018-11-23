import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import combinations

import sys
sys.path += ["C:/_CALLUM/Algorithmic Trading/Backtester/Basic for-loop"]

data = pd.read_csv("C:/_CALLUM/Algorithmic Trading/Backtester/Basic for-loop/clean_universe_stock_data.csv", header=[0,1], index_col = 0)
all_tickers = sorted(list(set(data.columns.get_level_values(0))))

class Strategy(object):

    """
    this is an ABC for strategies, used so methods can be created which apply to all strategies, like backtest
    """

    def __init__(self, ticker_list):
        
        self.ticker_list = ticker_list
        self.data = data[ticker_list]
        self.prices = pd.DataFrame(index=data.index)
        for ticker in ticker_list:
            self.prices[ticker] = self.data[ticker]["Adj Close"]
        self.prices_non_comp = self.prices.pct_change()[1:]
            
    def backtest(self):

        self.returns_non_comp = pd.DataFrame(index=self.trading_signals.index[:-1], columns=self.ticker_list)

        for ticker in self.ticker_list:
            
            for date in range(len(self.trading_signals) - 1):

                position_size = 1 / self.prices[ticker][date]
                closing_revenue = position_size * self.prices[ticker][date + 1]
                self.returns_non_comp[ticker][date] = closing_revenue

        return (self.prices_non_comp, self.returns_non_comp)
        

class Momentum(Strategy):

    """
    measures the sma and lma, goes long if sma > lma, short otherwise
    """

    def __init__(self, ticker_list, short_window, long_window):

        Strategy.__init__(self, ticker_list)

        self.short = short_window
        self.long = long_window

        self.short_ma = self.prices.rolling(short_window).mean()[long_window:]
        self.long_ma = self.prices.rolling(long_window).mean()[long_window:]

        self.trading_signals = 2*(self.short_ma > self.long_ma) - 1


def get_all_returns():

    """
    implements the Momentum strategy with a 10 day SMA and 30 day LMA on the entire ticker set, gets the correlation coefficient
    matrix for the prices and the returns, and returns a dictionary with the stock pairs as keys, and a tuple of prices correlation and 
    returns correlation as values
    """

    m = Momentum(all_tickers, 10, 30)
    btest = m.backtest()
    prices = btest[0]
    rets = btest[1]
    prices_corr = np.corrcoef(prices.T.astype(float))
    rets_corr = np.corrcoef(rets.T.astype(float))

    d = {}
    for i in combinations(range(prices_corr.shape[0]), 2):
        key = (all_tickers[i[0]], all_tickers[i[1]])
        vals = (prices_corr[i[0],i[1]], rets_corr[i[0],i[1]])
        d[key] = vals

    return d      
            
        
