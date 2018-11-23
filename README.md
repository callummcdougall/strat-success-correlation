# strat_success_correlation

strat_success_correlation is an exploration of the extent to which the success of a mean reversion strategy between major US equity stocks is shared across the market. This is not intended as a guide for investment, nor does it provide any hard statistical results, however it does identify a few very interesting patterns which warrant further exploration, and could potentiall (as I explain in the full writeup) yield practical applications.

In the future I am planning to transfer the article into a Medium blog post which will link to this Github page, but in the meantime I have kept all parts of my work, including code, graphs and writeup, in this repository.

# Repository contents

full_ticker_set.txt : A text file of all the ticker symbols used in my investigation. Note that some of these ended up having missing data points, so they weren't all included in the final results.

historical_prices_download.py : A python program which downloaded all the relevant data of the tickers in the full ticker set, cleaned the data and saved it to a csv file

signal_generation.py : A python program which tested a momentum strategy on the historical data, and generated my results

report.md : A full writeup of my investigations

returns_vs_price_corr_hist.png, returns_vs_price_corr_scatter.png : Graphs generated during my investigation, as described in report.md
