import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os
from stock import Stock

class Portfolio:
    
    def __init__(self, tickers, weights, period=10, start_date=None, end_date=None, quick_mode=False):
        self.ticker_names = tickers
        self.stocks = [Stock(ticker, quick_mode=quick_mode) for ticker in self.ticker_names]
        
        self.weights = weights      
        # in case tickers haven't been asigned weights. Lets face it, it's too tedious
        while (len(self.weights) < len(self.stocks)):
            self.weights.append(1)
       
        # initialize dates as None if no dates are provided     
        self.start_date = None
        self.end_date = None
        
        self.quick_mode=quick_mode
        
        # if no start_date or end_date has been input then calculate them by period
        if start_date == None and end_date == None:
            self.period = period
            self.start_date = (datetime.now() - relativedelta(years=period, days=1)).date()
            self.end_date = (datetime.now() - relativedelta(days=1)).date()
        else:
            if start_date != None:
                self.start_date = start_date
            else:
                self.start_date = (datetime.now() - relativedelta(years=period, days=1)).date()
            
            if end_date != None:
                self.end_date = end_date
            else:
                self.end_date = (datetime.now() - relativedelta(days=1)).date()

        self.adjustedReturns = self.calculateAdjustedReturns()
        self.averageAdjustedReturns = self.calculateAverageAdjustedReturns(self.adjustedReturns)
        self.weightsPercentage = [self.weights[i] / sum(self.weights) for i in range(len(self.weights))]
        
        # TODO: Fix sort by
        if not self.quick_mode:
            self.full_names = [i.stock_info["shortName"] for i in self.stocks]
            self.stocks_dataframe = pd.DataFrame(list(zip(self.ticker_names, self.adjustedReturns, self.weightsPercentage, self.full_names)), columns=["Ticker", "Returns", "Weights" , "Full name"]).sort_values(by="Returns", ascending=False)
            # print(self.stocks_dataframe)
    
    def printReturns(self):
        print(f"\nReturns {self.start_date} -> {self.end_date} or since IPO\n")
        print("TICKER".ljust(10) + "RETURNS%".rjust(10) + "WEIGTH%".rjust(10) + "\n")
        
        if not self.quick_mode:
            for i in range(len(self.stocks)):
                print(f"{self.stocks[i].ticker_name:10}{self.stocks[i].calculateAdjustedReturns(self.start_date):9.2f}%{self.weightsPercentage[i]*100:9.2f}%     {self.stocks[i].stock_info['shortName']:35}")
        else:
            for i in range(len(self.stocks)):
                print(f"{self.stocks[i].ticker_name:10}{self.stocks[i].calculateAdjustedReturns(self.start_date):9.2f}%{self.weightsPercentage[i]*100:9.2f}%")

        print(f"\nAverage returns: {self.averageAdjustedReturns:.2f}%\n")
    
    def plotPortfolio(self, p):
        # TODO: Plot portfolio returns
        for stock in self.stocks:
            stock.plotStock(str(self.start_date), p)
        # self.stocks[0].plotStock()
    
    def calculateAdjustedReturns(self):
        return [self.stocks[i].calculateAdjustedReturns(self.start_date) * self.weights[i] for i in range(len(self.stocks))]
    
    def calculateAverageAdjustedReturns(self, adjustedReturns) -> float:
        return sum(adjustedReturns) / len(self.stocks)
    
    # Getters
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