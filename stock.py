import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os
import ast

class Stock:
    
    def __init__(self, ticker, quick_mode=False):
        self.ticker_name = ticker
        self.ticker_filename = ticker.replace(".", "-")
        self.ticker = yf.Ticker(ticker)
        
        self.end_date = datetime.now().date() - relativedelta(days=1)
        
        self.price_data = self.loadPriceData()
        if not quick_mode:
            self.stock_info = self.loadStockInfo()
    
    def __repr__(self):
        return self.ticker_name
    
    def calculateAdjustedReturns(self, start) -> float:
        # if the date is to old for the stock data then find the first
        if start < datetime.strptime(self.price_data.first_valid_index(), "%Y-%m-%d").date():
            start = datetime.strptime(self.price_data.first_valid_index(), "%Y-%m-%d").date()

        # if the date doesn't exist, because of weekend etc, find next existing date
        while str(start) not in self.price_data.index:
            start += timedelta(days=1)
        
        try:
            first_price = self.price_data.loc[str(start)]
        except KeyError:
            print(f"The index doesn't exist: {start}")
            
        last_price = self.price_data.loc[self.price_data.last_valid_index()]
        
        return round((last_price - first_price) / first_price * 100, 2)

    def plotStock(self, start, p):
        plt.plot(self.price_data.loc[slice(start, str(self.end_date))][::10])
        plt.title(self.ticker_name)
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()
    
    # Methods used to load or cache data
    ####################################
    def loadPriceData(self): # -> Series eller DataFrame, oklart 
        if self.checkPriceDataCache():
            return pd.read_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", squeeze=True, index_col="Date")
        else:
            print(f"{self.ticker_name:8}: Price data is either non existing or outdated")
            self.cachePriceData()
            return pd.read_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", squeeze=True, index_col="Date")
            
    
    def downloadPriceData(self): # -> Series eller DataFrame, oklart
        print(f"{self.ticker_name:8}: Downloading price data")
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
            df = self.downloadPriceData()
            df.to_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", columns=["Adj Close"])
        else:
            if not self.checkPriceDataCache():
                print(f"{self.ticker_name:8}: Price data is not up to date")
                df = self.downloadPriceData()
                df.to_csv(f"./data/{self.ticker_filename}/{self.ticker_filename}_data.csv", sep=",", columns=["Adj Close"])
    
    def cacheStockInfo(self, force=False):
        if not os.path.exists(f"./data/{self.ticker_filename}/"): os.mkdir(f"./data/{self.ticker_filename}/")
        if not os.path.isfile(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt") or force:
            print(f"{self.ticker_name:8}: Downloading stock info")
            with open(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt", "w") as file:
                info = str(self.ticker.get_info())
                file.write(info)
        else:
            print(f"{self.ticker_name:8}: Stock info found")
            
    def loadStockInfo(self): # -> Series eller DataFrame, oklart 
        if os.path.isfile(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt"):
            with open(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt", "r") as file:
                return ast.literal_eval(file.read())
        else:
            print(f"{self.ticker_name:8}: Stock info is either non existing or outdated")
            self.cacheStockInfo()
            with open(f"./data/{self.ticker_filename}/{self.ticker_filename}_info.txt", "r") as file:
                return ast.literal_eval(file.read())