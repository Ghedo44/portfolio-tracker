import yfinance as yf
from typing import Union, List

def fetch_price(ticker):
    data = yf.Ticker(ticker).history(period='1d')
    return data['Close'].iloc[-1]

def fetch_prices(tickers):
    return {ticker: fetch_price(ticker) for ticker in tickers}

def fetch_historical_prices(tickers: Union[str, List], period="1mo", interval="1d", start = None, end = None):
    """
    Fetch historical prices for a given ticker

    period : str
        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Either Use period parameter or use start and end
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        Intraday data cannot extend last 60 days
    start: str
        Download start date string (YYYY-MM-DD) or _datetime, inclusive.
        Default is 99 years ago
        E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
    end: str
        Download end date string (YYYY-MM-DD) or _datetime, exclusive.
        Default is now
        E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
    """
    if period and not (start or end):
        data = yf.Ticker(tickers).history(period=period, interval=interval)
    else:
        data = yf.Ticker(tickers).history(start=start, end=end, interval=interval)
    return data