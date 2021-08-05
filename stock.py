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
        self.ticker_filename = ticker.replace(".", "-")
        self.ticker = yf.Ticker(ticker)
        
        self.end_date = datetime.now().date() - relativedelta(days=1)
        
        self.price_data = self.loadPriceData()
        self.stock_info = self.loadStockInfo()
    
    def __repr__(self):
        return self.ticker_name
    
    def calculateAdjustedReturns(self, start) -> float:
        if start < datetime.strptime(self.price_data.first_valid_index(), "%Y-%m-%d").date():
            # print(f"too early dude {start}")
            start = datetime.strptime(self.price_data.first_valid_index(), "%Y-%m-%d").date()
            # print(f"now {start}")
        
        first_price = self.price_data.loc[str(start)]
        last_price = self.price_data.loc[self.price_data.last_valid_index()]
        
        return round((last_price - first_price) / first_price * 100, 2)
    
    # Methods used to load or cache data
    ####################################
    def loadPriceData(self): # -> Series eller DataFrame, oklart 
        if self.checkPriceDataCache():
            return pd.read_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", squeeze=True, index_col="Date")
        else:
            print(f"{self.ticker_name:8} cache is either non existing or outdated - Downloading")
            self.cachePriceData()
            return pd.read_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", squeeze=True, index_col="Date")
            
    
    def downloadPriceData(self): # -> Series eller DataFrame, oklart
        return yf.download(self.ticker_name, period="max", end=self.end_date, progress=False)
    
    def checkPriceDataCache(self) -> bool:
        if os.path.isfile(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv"):
            comp = pd.read_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", squeeze=True, index_col="Date")
            if comp.last_valid_index() in [str(self.end_date), str(self.end_date - relativedelta(days=1)), str(self.end_date - relativedelta(days=2))]:
                return True
        return False
    
    def cachePriceData(self, force=False):
        if not os.path.exists(f"./data/{self.ticker_filename}/"): os.mkdir(f"./data/{self.ticker_filename}/")
        if not os.path.isfile(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv") or force:
            print(f"{self.ticker_name:8} caching")
            df = self.downloadPriceData()
            df.to_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", columns=["Adj Close"])
        else:
            if self.checkPriceDataCache():
                print(f"{self.ticker_name:8} stock data cache is up to date")
            else:
                print(f"{self.ticker_name:8} stock data cache is not up to date -> caching")
                df = self.downloadPriceData()
                df.to_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", columns=["Adj Close"])
    
    def cacheStockInfo(self, force=False):
        if not os.path.exists(f"./data/{self.ticker_filename}/"): os.mkdir(f"./data/{self.ticker_filename}/")
        if not os.path.isfile(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt") or force:
            print(f"{self.ticker_name:8} caching info")
            with open(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt", "w") as file:
                info = str(self.ticker.get_info())
                file.write(info)
        else:
            print(f"{self.ticker_name:8} info found in cache")
            
    def loadStockInfo(self): # -> Series eller DataFrame, oklart 
        if os.path.isfile(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt"):
            with open(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt", "r") as file:
                return ast.literal_eval(file.read())
        else:
            print(f"{self.ticker_name:8} info is either non existing or outdated - Downloading")
            self.cacheStockInfo()
            with open(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt", "r") as file:
                return ast.literal_eval(file.read())
            
# tickerNames = ["AAPL", "MSFT", "2222.SR", "GOOG", "AMZN", "FB", "TSLA", "BRK-A", "TSM", "TCEHY"]
# stocks = [Stock(ticker) for ticker in tickerNames]

# print(stocks)

# # for stock in stocks:
# #     print(stock)
# #     print(stock.stock_info)
# #     print(stock.stock_data)
    