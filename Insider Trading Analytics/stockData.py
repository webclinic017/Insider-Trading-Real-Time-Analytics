# Add real time stock data & moving average data

import pandas_datareader as dr
import pandas as pd
from datetime import datetime,date,timedelta

def getStockPrice(symbol,n=180):

    try:   
        tickerdf=dr.data.get_data_yahoo(symbol,start=date.today()-timedelta(300),end=date.today())
        currentprice=tickerdf.iloc[-1]["Close"]

        MA=pd.Series(tickerdf["Close"].rolling(n,min_periods=0).mean(),name='MA')
        currentMA=MA[-1]
        

        return (currentprice,currentMA)

    except:
        return(-1,-1)



    