from abc import ABC, abstractmethod
from pt.richtools import repr_rich
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.table import Table
from typing import List, Union, Dict

from .market_data import fetch_historical_prices, fetch_price

__all__ = ['Asset', 'Stock', 'ETF', 'Bond', 'Crypto', 'Assets', 'Cash']

class Asset(ABC):
    def __init__(self, name, currency: str = None):
        self.name = name
        self.currency = currency
        self.average_loading_price = 0
        self.amount = 0
        self.total_invested = 0
        self._price_history = None
        self._price = None

    @property
    def price(self) -> float:
        if self._price is None:
            self._price = fetch_price(self.name)
        return self._price

    @property
    def price_history(self) -> List[float]:
        if self._price_history is None:
            self._price_history = fetch_historical_prices(self.name, period="max", interval="1d")['Close'].tolist()
        return self._price_history

    def asset_type(self):
        return self.__class__.__name__

    @abstractmethod
    def calculate_value(self, price):
        pass

    # @abstractmethod
    # def calculate_performance(self):
    #     pass
    def calculate_performance(self):
        current_value = self.calculate_value(self.price)
        profit_loss = current_value - self.total_invested
        return {
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
        }

    def __rich__(self) -> str:
        # Create a table with the asset information
        table = Table(title=self.name, box=box.SIMPLE, show_header=False)
        table.add_column("Attribute")
        table.add_column("Value")
        table.add_row("Amount", str(self.amount))
        table.add_row("Total Invested", f"${self.total_invested:.2f}")
        table.add_row("Price", f"${self.price:.2f}")
        table.add_row("Currency", self.currency)
        return Panel(table, title="Asset Information")
        
    def __repr__(self):
        return repr_rich(self)

class Stock(Asset):
    def __init__(self, name, currency, dividends=0):
        super().__init__(name, currency)
        self.dividends = dividends

    def calculate_value(self, price):
        return self.amount * price

    # def calculate_performance(self):
    #     current_value = self.calculate_value(self.price)
    #     profit_loss = current_value - self.total_invested + self.dividends
    #     return {
    #         'current_value': current_value,
    #         'profit_loss': profit_loss,
    #         'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
    #     }

class ETF(Asset):
    def __init__(self, name, currency, annual_cost=0):
        super().__init__(name, currency)
        self.annual_cost = annual_cost

    def calculate_value(self, price):
        return self.amount * price

    # def calculate_performance(self):
    #     current_value = self.calculate_value(self.price)
    #     profit_loss = current_value - self.total_invested - self.annual_cost
    #     return {
    #         'current_value': current_value,
    #         'profit_loss': profit_loss,
    #         'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
    #     }

class Bond(Asset):
    def __init__(self, name, interest_rate=0):
        super().__init__(name)
        self.interest_rate = interest_rate

    def calculate_value(self, price):
        return self.amount * price

    # def calculate_performance(self):
    #     current_value = self.calculate_value(self.price)
    #     profit_loss = current_value - self.total_invested + (self.interest_rate * self.total_invested)
    #     return {
    #         'current_value': current_value,
    #         'profit_loss': profit_loss,
    #         'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
    #     }

class Crypto(Asset):
    def calculate_value(self, price):
        return self.amount * price

    # def calculate_performance(self):
    #     current_value = self.calculate_value(self.price)
    #     profit_loss = current_value - self.total_invested
    #     return {
    #         'current_value': current_value,
    #         'profit_loss': profit_loss,
    #         'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
    #     }


class Assets(dict):
    def __setitem__(self, key: str, value: Asset):
        if key in self:
            existing_asset = self[key]
            existing_asset.amount += value.amount
            existing_asset.average_loading_price = (existing_asset.total_invested + value.total_invested) / existing_asset.amount
            existing_asset.total_invested += value.total_invested
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key: str) -> Asset:
        return super().__getitem__(key)

    def filter(self, names: Union[str, List[str]]) -> 'Assets':
        if isinstance(names, str):
            names = [names]
        return Assets({name: self[name] for name in names if name in self})

    def add_asset(self, name, amount, total_invested, transaction_cost=0):
        if name in self:
            existing_asset = self[name]
            existing_asset.amount += amount
            existing_asset.total_invested += total_invested
        else:
            new_asset = Asset(name, transaction_cost)
            new_asset.amount = amount
            new_asset.total_invested = total_invested
            self[name] = new_asset

    def calculate_performance(self):
        performance = {}
        for asset_name, asset in self.items():
            performance[asset_name] = asset.calculate_performance()
        return performance

    def __rich__(self) -> str:
        table = Table(box=None, show_header=True)
        table.add_column("Asset Name")
        table.add_column("Amount")
        table.add_column("Total Invested")
        table.add_column("Price")
        table.add_column("Currency")
        
        for asset in self.values():
            table.add_row(
                asset.name,
                str(asset.amount),
                f"${asset.total_invested:.2f}",
                f"${asset.price:.2f}",
                asset.currency
            )

        return Panel(table, title="Assets")
    
    def __repr__(self):
        return repr_rich(self)


class Cash:
    def __init__(self, exchange_rates: Dict[str, Dict[str, float]] = None):
        # Holds the balance for each currency
        self.balances = {}  # e.g., {"EUR": 1000.0, "USD": 500.0}
        self.exchange_rates = exchange_rates or {}  # e.g., {"EUR": {"USD": 1.1, "GBP": 0.85}}

    def __getitem__(self, currency: str) -> float:
        """Return the balance for the given currency, defaulting to 0 if it doesn't exist"""
        return self.balances.get(currency, 0.0)

    def __setitem__(self, currency: str, amount: float):
        # Set the balance for the given currency
        if amount < 0:
            raise ValueError("Balance amount cannot be negative.")
        self.balances[currency] = amount

    def __delitem__(self, currency: str):
        # Remove the balance for the given currency
        if currency in self.balances:
            del self.balances[currency]
        else:
            raise KeyError(f"Currency {currency} not found.")
        
    def get(self, currency: str) -> float:
        """Return the balance for the given currency, defaulting to 0 if it doesn't exist"""
        return self.balances.get(currency, 0.0)
        
    def deposit(self, currency: str, amount: float):
        if amount > 0:
            if currency in self.balances:
                self.balances[currency] += amount
            else:
                self.balances[currency] = amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, currency: str, amount: float):
        if amount > 0:
            if currency in self.balances and self.balances[currency] >= amount:
                self.balances[currency] -= amount
            else:
                raise ValueError("Insufficient cash balance or currency not found.")
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def asset_bought(self, currency: str, amount: float, transaction_cost: float, transaction_cost_currency: str = None):
        transaction_cost_currency = transaction_cost_currency if transaction_cost_currency is not None else currency
        if amount > 0:
            if currency in self.balances and self.balances[currency] >= amount and self.balances[transaction_cost_currency] >= transaction_cost:
                if transaction_cost_currency == currency:
                    self.balances[currency] -= amount + transaction_cost
                else:
                    self.balances[currency] -= amount
                    self.balances[transaction_cost_currency] -= transaction_cost
            else:
                raise ValueError(f"Insufficient cash balance for {currency}.")
        else:
            raise ValueError("Transaction amount must be positive.")
        
    def asset_sold(self, currency: str, amount: float, transaction_cost: float, transaction_cost_currency: str = None):
        transaction_cost_currency = transaction_cost_currency if transaction_cost_currency is not None else currency
        if amount > 0:
            if transaction_cost_currency == currency:
                self.balances[currency] += amount - transaction_cost
            else:
                self.balances[currency] += amount
                self.balances[transaction_cost_currency] -= transaction_cost
        else:
            raise ValueError("Transaction amount must be positive.")


    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        if from_currency == to_currency:
            return amount
        elif from_currency in self.exchange_rates and to_currency in self.exchange_rates[from_currency]:
            rate = self.exchange_rates[from_currency][to_currency]
            return amount * rate
        else:
            raise ValueError(f"Exchange rate from {from_currency} to {to_currency} not available.")

    def total_balance(self, target_currency: str) -> float:
        total = 0.0
        for currency, balance in self.balances.items():
            total += self.convert(currency, target_currency, balance)
        return total

    def __str__(self):
        balances_str = ", ".join([f"{currency}: {balance:.2f}" for currency, balance in self.balances.items()])
        return f"Balances: {balances_str}"

    def __rich__(self):
        balances_str = "\n".join([f"{currency}: {balance:.2f}" for currency, balance in self.balances.items()])
        text = Text(balances_str)
        return Panel(text, title="Cash Balances")
    
    def __repr__(self):
        return repr_rich(self)
