from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import fix_yahoo_finance as yf
yf.pdr_override()

#set initial parameters

start_date = "2010-01-01"
end_date = "2015-01-01"
all_attr = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

#define function building stock data from yahoo finance

def build_stock_data(ticker_list, attr_list=all_attr, start=start_date, end=end_date):

    """
    builds data for all stocks in ticker list between start and end date

    returns: pd.DataFrame (or pd.Panel if ticker_list > 1)
    """

    all_data = pdr.get_data_yahoo(ticker_list, start, end)
    key_data = all_data[attr_list]
    key_data.ffill(inplace=True)

    return key_data

#import full ticker set, build stock data from all tickers with function above

import sys
sys.path += ["C:/_CALLUM/Algorithmic Trading/Backtester/Basic for-loop"]

import full_ticker_set
universe_ticker_set = full_ticker_set.sids
universe_ticker_list = [i[1] for i in universe_ticker_set]
data = build_stock_data(ticker_list=universe_ticker_list)

#clean + format the data, save it as a csv

data.index = data.iloc[:,0]
data = data.drop(data.columns[0], axis=1)

l = np.array(range(0,6*867,867))
l_2 = []
for i in range(867):
	l_2 += list(i + l)
data = data.iloc[:, l_2]

attr = list(data.columns[:6])
tickers = sorted(list(set(data.iloc[0, :])))

for ticker in tickers:
	if data.loc[:, ticker].isnull().values.any():
		data = data.drop(ticker, axis=1)

data.to_csv(r"C:/_CALLUM/Algorithmic Trading/Backtester/Basic for-loop/clean_universe_stock_data.csv")
m_index = pd.MultiIndex.from_product((tickers, attr), names=("tickers", "attr"))
data.columns = m_index
data = data.iloc[2:]
