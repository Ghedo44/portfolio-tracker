import yfinance as yf
import pandas as pd

__all__ = ['get_stock_data']

def get_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    data = stock.history(start=start, end=end)
    return data

def get_live_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    return stock.history(period='1d').iloc[-1]['Close']