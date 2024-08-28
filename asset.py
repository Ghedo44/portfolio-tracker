from abc import ABC, abstractmethod
from richtools import repr_rich
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.table import Table

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
