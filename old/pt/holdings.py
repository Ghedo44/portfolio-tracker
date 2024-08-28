from typing import List

__all__ = ['Stock', 'Cash', 'Bond']

class Stock:
    def __init__(self, symbol, shares, price):
        self.symbol = symbol
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price
    
    def sell(self, nshares):
        self.shares -= nshares
        
    def __repr__(self):
        return f'Stock({self.symbol!r}, {self.shares}, {self.price})'
    

class Stocks:
    def __init__(self, stocks: List[Stock]):
        self.stocks = stocks
        
    def __getitem__(self, symbol):
        for stock in self.stocks:
            if stock.symbol == symbol:
                return stock
        raise KeyError(symbol)
    
    def __iter__(self):
        return iter(self.stocks)
    
    def __repr__(self):
        return f'Stocks({self.stocks})'
    
    def cost(self):
        return sum(stock.cost() for stock in self.stocks)
    
    def sell(self, symbol, nshares):
        self[symbol].sell(nshares)
        
    def __len__(self):
        return len(self.stocks)
    
    def __contains__(self, symbol):
        return any(stock.symbol == symbol for stock in self.stocks)
    
    def __getitem__(self, symbol):
        for stock in self.stocks:
            if stock.symbol == symbol:
                return stock
        raise KeyError(symbol)
    
    def __setitem__(self, symbol, stock):
        for i, s in enumerate(self.stocks):
            if s.symbol == symbol:
                self.stocks[i] = stock
                return
        self.stocks.append(stock)
        
    def __delitem__(self, symbol):
        for i, stock in enumerate(self.stocks):
            if stock.symbol == symbol:
                del self.stocks[i]
                return
        raise KeyError(symbol)
    
    def __repr__(self):
        return f'Stocks({self.stocks})'
    
    
class Cash:
    def __init__(self, amount):
        self.amount = amount
        
    def __repr__(self):
        return f'Cash({self.amount})'
    
    def cost(self):
        return self.amount
    
    def sell(self, nshares):
        self.amount -= nshares
     
       
class Bond:
    def __init__(self, symbol, shares, price):
        self.symbol = symbol
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price
    
    def sell(self, nshares):
        self.shares -= nshares
        
    def __repr__(self):
        return f'Bond({self.symbol!r}, {self.shares}, {self.price})'