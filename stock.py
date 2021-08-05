import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os
import ast

class Stock:
    
    def __init__(self, ticker):
        self.ticker_name = ticker
        self.ticker = yf.Ticker(ticker)
        
        self.end_date = datetime.now().date() - relativedelta(days=1)
        
        self.stock_data = self.loadStockData()
        self.stock_info = self.loadStockInfo()
    
    def __repr__(self):
        return self.ticker_name
    
    def loadStockData(self): # -> Series eller DataFrame, oklart 
        if self.checkStockDataCache():
            return pd.read_csv(f"./data/{self.ticker_name}/{self.ticker_name}_data.csv", sep=",", squeeze=True, index_col="Date")
        else:
            print(f"{self.ticker_name:8} cache is either non existing or outdated - Downloading")
            return self.cacheStockData()
    
    def downloadStockData(self): # -> Series eller DataFrame, oklart
        return yf.download(self.ticker_name, period="max", end=self.end_date, progress=False)
    
    def checkStockDataCache(self) -> bool:
        if os.path.isfile(f"./data/{self.ticker_name}/{self.ticker_name}_data.csv"):
            comp = pd.read_csv(f"./data/{self.ticker_name}/{self.ticker_name}_data.csv", sep=",", squeeze=True, index_col="Date")
            if comp.last_valid_index() in [str(self.end_date), str(self.end_date - relativedelta(days=1)), str(self.end_date - relativedelta(days=2))]:
                return True
        return False
    
    def cacheStockData(self, force=False):
        if not os.path.isfile(f"./data/{self.ticker_name}/{self.ticker_name}_data.csv") or force:
            print(f"{self.ticker_name:8} caching")
            df = self.downloadStockData()
            df.to_csv(f"./data/{self.ticker_name}/{self.ticker_name}_data.csv", sep=",", columns=["Adj Close"])
            return df
        else:
            if self.checkStockDataCache():
                print(f"{self.ticker_name:8} stock data cache is up to date")
            else:
                print(f"{self.ticker_name:8} stock data cache is not up to date -> caching")
                df = self.downloadStockData()
                df.to_csv(f"./data/{self.ticker_name}/{self.ticker_name}_data.csv", sep=",", columns=["Adj Close"])
                return df
    
    def cacheStockInfo(self, force=False):
        if not os.path.exists(f"./data/{self.ticker_name}/"): os.mkdir(f"./data/{self.ticker_name}/")
        if not os.path.isfile(f"./data/{self.ticker_name}/{self.ticker_name}_info.txt") or force:
            print(f"{self.ticker_name:8} caching info")
            with open(f"./data/{self.ticker_name}/{self.ticker_name}_info.txt", "w") as file:
                info = str(self.ticker.get_info())
                file.write(info)
                return info
        else:
            print(f"{self.ticker_name:8} info found in cache")
            
    def loadStockInfo(self): # -> Series eller DataFrame, oklart 
        if os.path.isfile(f"./data/{self.ticker_name}/{self.ticker_name}_info.txt"):
            with open(f"./data/{self.ticker_name}/{self.ticker_name}_info.txt", "r") as file:
                return ast.literal_eval(file.read())
        else:
            print(f"{self.ticker_name:8} info is either non existing or outdated - Downloading")
            return self.cacheStockInfo()
            
tickerNames = ["AAPL", "MSFT", "2222.SR", "GOOG", "AMZN", "FB", "TSLA", "BRK-A", "TSM", "TCEHY"]
stocks = [Stock(ticker) for ticker in tickerNames]

print(stocks)

# for stock in stocks:
#     print(stock)
#     print(stock.stock_info)
#     print(stock.stock_data)
    