from abc import ABC, abstractmethod
from pt.richtools import repr_rich
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.table import Table
from typing import List

from .market_data import fetch_historical_prices, fetch_price

class Asset(ABC):
    def __init__(self, name, currency: str = None):
        self.name = name
        self.currency = currency
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
    def __setitem__(self, key, value):
        if not isinstance(value, Asset):
            raise ValueError("Value must be an instance of Asset")

        if key in self:
            existing_asset = self[key]
            existing_asset.amount += value.amount
            existing_asset.total_invested += value.total_invested
        else:
            super().__setitem__(key, value)

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
    def __init__(self, amount):
        self.amount = amount

    def __rich__(self) -> str:
        return Panel(Text(f"Amount: ${self.amount:.2f}"), title="Cash")
    
    def __repr__(self):
        return repr_rich(self)