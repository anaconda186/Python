import datetime as dt

import pandas_datareader.data as pdr

end = dt.datetime.today()
start = dt.datetime.today() - dt.timedelta(days=365)

stock_history = {}
stock_list = []
with open("S&P500_list.csv") as list:
    for line in list:
        stock = line.strip().split(",")[0]
        stock_list.append(stock)
        df = pdr.DataReader(str(stock), "yahoo", start=start, end=end)
        stock_history[f"{stock}"] = df["Close"]


print(stock_history)
print(stock_list)
