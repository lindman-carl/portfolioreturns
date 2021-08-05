import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os
from stock import Stock

class Portfolio:
    
    def __init__(self, tickers, weights, period):
        self.ticker_names = tickers
        self.stocks = [Stock(ticker) for ticker in self.ticker_names]
        
        # self.tickersInfo = self.loadTickerInfo()
        
        self.weights = weights
        while (len(self.weights) < len(self.stocks)):
            self.weights.append(1)
        
        self.period = period

        self.start_date = (datetime.now() - relativedelta(years=period, days=1)).date()
        self.end_date = (datetime.now() - relativedelta(days=1)).date()
        
        # self.data = yf.download(tickers=self.ticker_names, start=self.start_date, end=self.end_date, group_by=["Ticker", "Date"], progress=False)
        
        # self.adjustedReturns = [self.calculateAdjustedReturns(self.data[x]) * self.weights[i] for i, x in enumerate(self.ticker_names)]
        # self.averageAdjustedReturns = self.calculateAverageAdjustedReturns()
        self.weightsPercentage = [self.weights[i] / sum(self.weights) for i in range(len(self.weights))]

    def loadTickerInfo(self):
        print("Loading data...\n")
        return [self.tickers.tickers[self.ticker_names[i]].info for i in range(len(self.ticker_names)-1)]

    def calculateReturns(self, data) -> float:
        first_price = data["Close"].loc[data.first_valid_index()]
        last_price = data["Close"].loc[data.last_valid_index()]
        
        return (last_price - first_price) / first_price * 100

    def calculateAdjustedReturns(self) -> float:
        # returns = 0.0
        # for i in range(len(self.stocks)):
        #     returns += self.stocks[i] * self.weights[i]
        
        # return returns
        pass
    
    def printReturns(self):

        print(f"Returns {self.start_date} -> {self.end_date} ({self.period} years) or since IPO\n")

        print("TICKER".ljust(10) + "RETURNS%".rjust(10) + "WEIGTH%".rjust(10) + "\n")
        
        for i in range(len(self.stocks)):
            print(f"{self.stocks[i].ticker_name:10}{self.stocks[i].calculateAdjustedReturns(self.start_date):9.2f}%{self.weightsPercentage[i]*100:9.2f}%    {self.stocks[i].stock_info['shortName']}")

        print(f"\nAverage returns: {self.calculateAverageAdjustedReturns():.2f}%\n")
    
    def plotPortfolio(self):
        # returnsDF = 
        print(self.data.index)
        
    def saveStocksAsCsv(self):
        for ticker in self.ticker_names:
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
                
        
    def calculateAverageAdjustedReturns(self) -> float:
        return sum([self.stocks[i].calculateAdjustedReturns(self.start_date) * self.weights[i] for i in range(len(self.stocks))]) / len(self.stocks)
    
    def getAdjustedReturns(self) -> list:
        return self.adjustedReturns
    
    def getAverageAdjustedReturns(self) -> float:
        return self.averageAdjustedReturns
    
    def getWeightsPercentage(self) -> list:
        return self.weightsPercentage
    
    def getStartDate(self) -> datetime.date:
        return self.start_date
    
    def getEndDate(self) -> datetime.date:
        return self.end_date