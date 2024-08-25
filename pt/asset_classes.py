from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Union
import requests  # For fetching market data, you may use an API library

# Abstract Base Class for Assets
class Asset(ABC):
    def __init__(self, symbol: str, quantity: float):
        self.symbol = symbol
        self.quantity = quantity
        self.transactions = []  # Stores all transactions for this asset

    @abstractmethod
    def update_price(self):
        pass

    @abstractmethod
    def calculate_value(self):
        pass

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

class Equity(Asset):
    def __init__(self, symbol: str, quantity: float, price: float):
        super().__init__(symbol, quantity)
        self.price = price

    def update_price(self):
        # API call to update price
        self.price = self.fetch_price_from_api()

    def fetch_price_from_api(self):
        # Use an API like Yahoo Finance to fetch the latest price
        # This is a placeholder, implement with actual API logic
        return requests.get(f"https://api.example.com/price/{self.symbol}").json()["price"]

    def calculate_value(self):
        return self.quantity * self.price

class ETP(Equity):
    """
    Exchange-Traded Product (ETP) is a type of security that is derivatively priced and traded on a stock exchange.
    It can track an underlying asset, index, or financial instrument.
    Types of ETPs include ETFs, ETNs, and ETCs.
    """
    def __init__(self, symbol: str, quantity: float, price: float, expense_ratio: float, underlying_assets: Dict[str, float] = None):
        super().__init__(symbol, quantity, price)
        self.expense_ratio = expense_ratio  # Annual fee as a percentage
        self.underlying_assets = underlying_assets if underlying_assets else {}  # e.g., {'AAPL': 25%, 'MSFT': 20%}

    def calculate_value(self):
        # Adjust value for expense ratio
        value = super().calculate_value()
        return value * (1 - self.expense_ratio)

    def list_underlying_assets(self):
        return self.underlying_assets

    def update_price(self):
        # You can extend this to simulate how underlying assets affect ETF value
        super().update_price()

# Example Usage
# vanguard_etf = ETF(symbol="VOO", quantity=20, price=400, expense_ratio=0.03, 
#                    underlying_assets={"AAPL": 25, "MSFT": 20, "GOOGL": 15})


class Crypto(Asset):
    def __init__(self, symbol: str, quantity: float):
        super().__init__(symbol, quantity)
        self.price = 0

    def update_price(self):
        # Example logic for fetching crypto prices
        self.price = self.fetch_price_from_crypto_api()

    def fetch_price_from_crypto_api(self):
        # Implement the API logic here
        return requests.get(f"https://api.crypto.com/price/{self.symbol}").json()["price"]

    def calculate_value(self):
        return self.quantity * self.price




class Cash:
    def __init__(self, currency: str = "EUR"):
        self.currency = currency
        self.balance = 0.0
        self.interest_rate = 0.0  # Annual interest rate for cash

    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount: float):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
            else:
                raise ValueError("Insufficient cash balance.")
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def apply_interest(self):
        # This function could be called periodically (e.g., monthly or annually)
        self.balance += self.balance * (self.interest_rate / 12)  # Assuming monthly interest accrual

    def __str__(self):
        return f"Cash Balance: {self.balance:.2f} {self.currency}"

# Example Usage
# cash_account = Cash(currency="USD")
# cash_account.deposit(10000)
# cash_account.apply_interest()  # Simulate interest accrual
# print(cash_account)