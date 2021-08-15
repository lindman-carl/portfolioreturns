from portfolio import Portfolio
import time
import sys
import os
import argparse
from datetime import date


class PortfolioCalculator:

    def __init__(self) -> None:
        self.tickers = ["AAPL", "MSFT", "2222.SR", "GOOG",
                        "AMZN", "FB", "TSLA", "BRK-A", "TSM", "TCEHY"]
        self.weights = [1 for x in range(len(self.tickers))]
        self.period = 10
        self.start_date = None
        self.end_date = None
        self.quick_mode = False

    def parseArgv(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--filename", metavar="",
                            help="File containing tickers", type=str)
        parser.add_argument("-p", "--period", metavar="",
                            help="Years ago to calculate returns from", type=int)
        parser.add_argument("-sd", "--startdate", metavar="",
                            help="Date to calculate returns since", type=date.fromisoformat)
        parser.add_argument("-ed", "--enddate", metavar="",
                            help="Date to calculate returns until", type=date.fromisoformat)
        parser.add_argument("-l", "--list", metavar="",
                            help="List tickers seperated by ,", type=str)
        parser.add_argument("-q", "--quickmode", metavar="",
                            help="Set quickmode to True to speed up downloading a lot by not scraping company data", type=bool)
        parser.add_argument("-s", "--sortby", metavar="",
                            help="Sort by: r: returns, n:name, w:weight", type=str)
        args = parser.parse_args()

        if args.filename != None:
            try:
                with open(file=args.filename, mode="r") as file:
                    self.tickers = list(file.readline().strip("\n").split(","))
                    self.weights = [float(x)
                                    for x in file.readline().split(",")]
            except EnvironmentError:
                print("Couldn't load tickers from file")

        if args.list != None:
            try:
                self.tickers = list(args.list.split(","))
            except:
                print("Couldn't parse argument as list")

        if args.period != None:
            self.period = args.period

        if args.startdate != None:
            self.start_date = args.startdate

        if args.enddate != None:
            self.end_date = args.enddate

        if args.quickmode == True:
            self.quick_mode = True
        
        if args.sortby != None:
            if args.sortby.lower() == "r":
                # sort by returns
                pass
            elif args.sortby.lower() == "n":
                # sort by name, which is also default
                pass
            elif args.sortby.lower() == "w":
                # sort by portfolio weigth
                pass

    def run(self):
        start_runtime = time.time()  # for calculating runtime
        self.parseArgv()
        
        # print header
        print("\n" + "="*50)
        print("="*10 + " PORTFOLIO RETURNS CALCULATOR " + "="*10)
        print("="*50 + "\n")

        portfolio = Portfolio(self.tickers, self.weights, period=self.period,
                              start_date=self.start_date, end_date=self.end_date, quick_mode=self.quick_mode)
        portfolio.printReturns()

        print("="*20 + f" {time.time() - start_runtime:.5f}s " + "="*20)


if __name__ == "__main__":
    portfolio_calculator = PortfolioCalculator()
    portfolio_calculator.run()
