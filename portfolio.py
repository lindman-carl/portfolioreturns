import pandas as pd
import yfinance as yf
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Portfolio:
    
    def __init__(self, tickers, weights, period):
        self.tickers = yf.Tickers(tickers)
        self.tickerNames = list(self.tickers.tickers.keys())
        # self.tickersInfo = self.loadTickerInfo()
        
        self.weights = weights
        self.period = period

        self.start_date = datetime.now() - relativedelta(years=period)
        self.end_date = datetime.now()
        
        self.data = yf.download(tickers=self.tickerNames, start=self.start_date, end=self.end_date, group_by="Ticker", progress=False)

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

        print(f"\nAverage returns: {self.averageAdjustedReturns:.2f}%")

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