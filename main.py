from portfolio import Portfolio
import time
import sys
import os

def parseArgv() -> tuple:
    # some variable values
    tickers = ["AAPL", "MSFT", "2222.SR", "GOOG", "AMZN", "FB", "TSLA", "BRK-A", "TSM", "TCEHY"]
    tickers_10 = ["AAPL", "XOM", "0857.HK", "IBM", "MSFT", "1398.HK", "0941.HK", "RDSA.AS", "NESN.SW", "CVX"]
    tickers_20 = ["GE", "CSCO", "XOM", "PFE", "MSFT", "WMT", "C", "VOD.L", "INTC", "RDSA.AS"]
    weights = [1 for x in range(len(tickers))]  
    period = 10
    
    # if arguments is given
    if len(sys.argv) > 1:
        # if argrument is a file
        if (os.path.isfile(sys.argv[1])):
            # load and parse csv
            with open(file=sys.argv[1], mode="r") as file:
                tickers = list(file.readline().strip("\n").split(","))
                weights = [float(x) for x in file.readline().split(",")]
        else:
            # get tickers from list
            tickers = list(sys.argv[1].split(","))
    if len(sys.argv) > 2:
        period = int(sys.argv[2])
    
    return tickers, weights, period
    

if __name__ == "__main__":
    start_runtime = time.time() # for calculating runtime
    print("\n" + "="*10 + " PORTFOLIO RETURNS CALCULATOR " + "="*10 + "\n")
    tickers, weights, period = parseArgv()
    
    portfolio = Portfolio(tickers, weights, period)
    portfolio.printReturns()

    print("="*20 + f" {time.time() - start_runtime:.5f}s " + "="*20)