import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr


def buy_sell(signal):

    money = 10000
    stock_count = 0
    value = []
    buy = []
    sell = []
    flag = 0

    for i in range(0, len(signal)):
        if signal["MACD"][i] > signal["Signal Line"][i]:
            sell.append(np.nan)
            if flag != 1:
                buy.append(signal["Close"][i])
                flag = 1
                stock_count = money / signal["Close"][i]
                money = 0
            else:
                buy.append(np.nan)
        elif signal["MACD"][i] < signal["Signal Line"][i]:
            buy.append(np.nan)
            if flag != 0:
                sell.append(signal["Close"][i])
                flag = 0
                money = stock_count * signal["Close"][i]
                stock_count = 0
            else:
                sell.append(np.nan)

        else:
            sell.append(np.nan)
            buy.append(np.nan)
        value.append("${:,.2f}".format(stock_count * signal["Close"][i] + money))
    return (buy, sell, value)


end = dt.datetime.today()
start = dt.datetime.today() - dt.timedelta(days=365)

### Get Data ###

history_list = []
with open("S&P500_list.csv") as list:
    count = 0
    for line in list:
        stock = line.strip().split(",")[0]
        df = pdr.DataReader(str(stock), "yahoo", start=start, end=end)
        # df.head()
        short_term_EMA = df.Close.ewm(span=12, adjust=False).mean()
        long_term_EMA = df.Close.ewm(span=26, adjust=False).mean()
        macd = short_term_EMA - long_term_EMA
        signal_line = macd.ewm(span=9, adjust=False).mean()
        df["Name"] = str(stock)
        df["MACD"] = macd
        df["Signal Line"] = signal_line
        a = buy_sell(df)
        df["Buy Price"] = a[0]
        df["Sell Price"] = a[1]
        df["Value"] = a[2]

        history_list.append(df)
        count += 1

    results = pd.concat(history_list)
    results = results.sort_values(by=["Date", "Name"])
    results.to_csv("stock.csv")


### Function to determine Buy/Sell ###


# print(df)
# ### Plot Data ###

# plt.plot(df.index, df["Close"], label="Close", color="black")
# plt.scatter(df.index, df["Buy Price"], color="green", label="buy", marker="^", alpha=1)
# plt.scatter(df.index, df["Sell Price"], color="red", label="sell", marker="v", alpha=1)
# plt.legend(loc="upper left")
# plt.title("Close Price History")
# plt.xticks(rotation=45)
# plt.xlabel("Date")
# plt.ylabel("Price USD ($)")
# plt.show()
