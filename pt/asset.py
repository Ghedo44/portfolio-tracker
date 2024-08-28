from abc import ABC, abstractmethod
from pt.richtools import repr_rich
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.table import Table
from typing import List

class Asset(ABC):
    def __init__(self, name, transaction_cost=0):
        self.name = name
        self.transaction_cost = transaction_cost
        self.amount = 0
        self.total_invested = 0

    @abstractmethod
    def calculate_value(self, price):
        pass

    @abstractmethod
    def calculate_performance(self, current_price):
        pass

    def __rich__(self) -> str:
        # Create a table with the asset information
        table = Table(title=self.name, box=box.SIMPLE, show_header=False)
        table.add_column("Attribute")
        table.add_column("Value")
        table.add_row("Amount", str(self.amount))
        table.add_row("Total Invested", f"${self.total_invested:.2f}")
        table.add_row("Transaction Cost", f"${self.transaction_cost:.2f}")
        return Panel(table)
        
    def __repr__(self):
        return repr_rich(self)

class Stock(Asset):
    def __init__(self, name, transaction_cost=0, dividends=0):
        super().__init__(name, transaction_cost)
        self.dividends = dividends

    def calculate_value(self, price):
        return self.amount * price

    def calculate_performance(self, current_price):
        current_value = self.calculate_value(current_price)
        profit_loss = current_value - self.total_invested + self.dividends
        return {
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
        }

class ETF(Asset):
    def __init__(self, name, transaction_cost=0, annual_cost=0):
        super().__init__(name, transaction_cost)
        self.annual_cost = annual_cost

    def calculate_value(self, price):
        return self.amount * price

    def calculate_performance(self, current_price):
        current_value = self.calculate_value(current_price)
        profit_loss = current_value - self.total_invested - self.annual_cost
        return {
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
        }

class Bond(Asset):
    def __init__(self, name, transaction_cost=0, interest_rate=0):
        super().__init__(name, transaction_cost)
        self.interest_rate = interest_rate

    def calculate_value(self, price):
        return self.amount * price

    def calculate_performance(self, current_price):
        current_value = self.calculate_value(current_price)
        profit_loss = current_value - self.total_invested + (self.interest_rate * self.total_invested)
        return {
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
        }

class Crypto(Asset):
    def calculate_value(self, price):
        return self.amount * price

    def calculate_performance(self, current_price):
        current_value = self.calculate_value(current_price)
        profit_loss = current_value - self.total_invested
        return {
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': (profit_loss / self.total_invested) * 100 if self.total_invested > 0 else 0
        }

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
        table = Table(title="Assets Portfolio", box=None, show_header=True)
        table.add_column("Asset Name")
        table.add_column("Amount")
        table.add_column("Total Invested")
        table.add_column("Transaction Cost")
        
        for asset in self.values():
            table.add_row(
                asset.name,
                str(asset.amount),
                f"${asset.total_invested:.2f}",
                f"${asset.transaction_cost:.2f}"
            )

        return Panel(table)
    
    def __repr__(self):
        return repr_rich(self)
