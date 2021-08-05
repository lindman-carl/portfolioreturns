import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os

class Stock:
    
    def __init__(self, ticker):
        self.tickerName = ticker
        self.ticker = yf.Ticker(ticker)
    
    def checkCache(self):
        if os.path.isfile(f"./data/{self.tickerName}/{self.tickerName}_data.csv"):
            # check if cache is up to date
            pass

class Portfolio:
    
    def __init__(self, tickers, weights, period):
        self.tickers = yf.Tickers(tickers)
        self.tickerNames = list(self.tickers.tickers.keys())
        # self.tickersInfo = self.loadTickerInfo()
        
        self.weights = weights
        self.period = period

        self.start_date = datetime.now() - relativedelta(years=period, days=1)
        self.end_date = datetime.now() - relativedelta(days=1)
        
        self.data = yf.download(tickers=self.tickerNames, start=self.start_date, end=self.end_date, group_by=["Ticker", "Date"], progress=False)
        # self.data["diff"] = (self.data["Adj Close"] - self.data["Adj Close"].loc(self.data.first_valid_index()))
        # print(self.data["diff"])
        self.returns = [self.calculateReturns(self.data[x]) * self.weights[i] for i, x in enumerate(self.tickerNames)]
        self.adjustedReturns = [self.calculateAdjustedReturns(self.data[x]) * self.weights[i] for i, x in enumerate(self.tickerNames)]
        self.averageReturns = self.calculateAverageReturns()
        self.averageAdjustedReturns = self.calculateAverageAdjustedReturns()
        self.weightsPercentage = [self.weights[i] / sum(self.weights) for i in range(len(self.weights))]

    def loadTickerInfo(self):
        print("Loading data...\n")
        return [self.tickers.tickers[self.tickerNames[i]].info for i in range(len(self.tickerNames)-1)]

    def calculateReturns(self, data) -> float:
        first_price = data["Close"].loc[data.first_valid_index()]
        last_price = data["Close"].loc[data.last_valid_index()]
        
        return (last_price - first_price) / first_price * 100

    def calculateAdjustedReturns(self, data) -> float:
        first_price = data["Adj Close"].loc[data.first_valid_index()]
        last_price = data["Adj Close"].loc[data.last_valid_index()]
        
        return round((last_price - first_price) / first_price * 100, 2)
    
    def printReturns(self):

        print(f"Returns {self.start_date.date()} -> {self.end_date.date()} ({self.period} years) or since IPO\n")

        print("TICKER".ljust(8) + "RETURNS".rjust(12) + "PORTFOLIO%".rjust(12) + "\n")
        for i in range(len(self.tickerNames)):
            # print(f"{self.tickers.tickers[self.tickerNames[i]].info['shortName']}")
            print(f"{self.tickerNames[i]:8}{self.adjustedReturns[i]:11.2f}%{self.weightsPercentage[i]*100:11.2f}%")

        print(f"\nAverage returns: {self.averageAdjustedReturns:.2f}%\n")
    
    def plotPortfolio(self):
        # returnsDF = 
        print(self.data.index)
        
    def saveStocksAsCsv(self):
        for ticker in self.tickerNames:
            # dropna
            # self.data[ticker].dropna(subset=["Adj Close"]).to_csv(path_or_buf=f"./data/{ticker}_data.csv", columns=["Adj Close"]) 
            if not os.path.exists(f"./data/{ticker}/"): os.mkdir(f"./data/{ticker}/")
            if not os.path.isfile(f"./data/{ticker}/{ticker}_data.csv"):
                print(f"{ticker} saving cache1")
                self.data[ticker].to_csv(path_or_buf=f"./data/{ticker}/{ticker}_data.csv", columns=["Adj Close"])
            else:
                compare = pd.read_csv(f"./data/{ticker}/{ticker}_data.csv", sep=",", index_col="Date", squeeze=True)
                # print(type(compare))
                # print(compare)
                # print(type(self.data[ticker].get("Adj Close")))
                # print(self.data[ticker].get("Adj Close"))

                if self.data[ticker].get("Adj Close").equals(compare):
                    print(f"{ticker} data is already cached")
                else:
                    print(f"{ticker} saving cache2")
                    self.data[ticker].to_csv(path_or_buf=f"./data/{ticker}/{ticker}_data.csv", columns=["Adj Close"])
                

    def calculateAverageReturns(self) -> float:
        return sum(self.returns) / len(self.returns)
        
    def calculateAverageAdjustedReturns(self) -> float:
        return sum(self.adjustedReturns) / len(self.adjustedReturns)
        
    def getReturns(self) -> list:
        return self.returns
    
    def getAdjustedReturns(self) -> list:
        return self.adjustedReturns
    
    def getAverageReturns(self) -> float:
        return self.averageReturns
    
    def getAverageAdjustedReturns(self) -> float:
        return self.averageAdjustedReturns
    
    def getWeightsPercentage(self) -> list:
        return self.weightsPercentage
    
    def getStartDate(self) -> datetime.date:
        return self.start_date.date()
    
    def getEndDate(self) -> datetime.date:
        return self.end_date.date()