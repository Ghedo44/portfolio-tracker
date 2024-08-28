from datetime import datetime
from pt.asset import Asset

from .richtools import repr_rich
from rich import box
from rich.panel import Panel
from rich.table import Table
from typing import List


class Transaction:
    def __init__(self, asset: Asset, type: str, amount: int, price: float, date=None):
        self.asset = asset
        self.type = type  # 'buy' or 'sell'
        self.amount = amount
        self.price = price
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_csv_row(self):
        return [self.asset.name, self.type, self.amount, self.price, self.date]
    
    def __rich__(self):
        # Create a table with the transaction information
        table = Table(title=self.asset.name, box=box.SIMPLE, show_header=False)
        table.add_column("Attribute")
        table.add_column("Value")
        table.add_row("Type", self.type)
        table.add_row("Amount", str(self.amount))
        table.add_row("Price", f"${self.price:.2f}")
        table.add_row("Date", self.date)
        return Panel(table)
    
    def __repr__(self):
        return repr_rich(self)

class Transactions(list):
    def __init__(self, *args, transactions_per_page=20):
        if any(not isinstance(transaction, Transaction) for transaction in args):
            raise ValueError("Only Transaction objects can be appended")
        super().__init__(*args)
        self.transactions_per_page = transactions_per_page
        self._current_page = None

    @property
    def current_page(self):
        if self._current_page is None:
            self._current_page = self.total_pages()
        return self._current_page
    
    def append(self, transaction):
        if not isinstance(transaction, Transaction):
            raise ValueError("Only Transaction objects can be appended")
        super().append(transaction)

    def add_transaction(self, asset_name, amount, price, transaction_type):
        transaction = Transaction(asset_name, amount, price, transaction_type)
        self.append(transaction)

    def filter_by_asset(self, asset_name):
        return [transaction for transaction in self if transaction.name == asset_name]

    def first_page(self):
        self._current_page = 1
        return self.__repr__()

    def last_page(self):
        self._current_page = self.total_pages()
        return self.__repr__()

    def next_page(self):
        if self.current_page < self.total_pages():
            self._current_page += 1
            return self.__repr__()
        else:
            print("No more pages")

    def previous_page(self):
        if self.current_page > 1:
            self._current_page -= 1
            return self.__repr__()
        else:
            print("No more pages")

    def set_page(self, page_number):
        if 1 <= page_number <= self.total_pages():
            self._current_page = page_number

    def total_pages(self):
        return (len(self) + self.transactions_per_page - 1) // self.transactions_per_page

    def get_paginated_transactions(self):
        start = (self.current_page - 1) * self.transactions_per_page
        end = start + self.transactions_per_page
        return self[start:end]

    def __rich__(self) -> str:
        table = Table(title=f"Transactions (Page {self.current_page}/{self.total_pages()})", box=None, show_header=True)
        table.add_column("Asset Name")
        table.add_column("Amount")
        table.add_column("Price")
        table.add_column("Type")
        table.add_column("Date")

        for transaction in self.get_paginated_transactions():
            table.add_row(
                transaction.asset.name,
                str(transaction.amount),
                f"${transaction.price:.2f}",
                transaction.type,
                transaction.date
            )

        return Panel(table)

    def __repr__(self):
        return repr_rich(self)

# class Transactions(list):
#     def append(self, transaction):
#         if not isinstance(transaction, Transaction):
#             raise ValueError("Only Transaction objects can be appended")
#         super().append(transaction)

#     def add_transaction(self, asset_name, amount, price, transaction_type):
#         transaction = Transaction(asset_name, amount, price, transaction_type)
#         self.append(transaction)

#     def filter_by_asset(self, asset_name):
#         return [transaction for transaction in self if transaction.asset_name == asset_name]

#     def __rich__(self):
#         table = Table(title="Transactions", box=box.SIMPLE, show_header=True)
#         table.add_column("Asset")
#         table.add_column("Type")
#         table.add_column("Amount")
#         table.add_column("Price")
#         table.add_column("Date")
#         for transaction in self:
#             table.add_row(transaction.asset.name, transaction.type, str(transaction.amount), f"${transaction.price:.2f}", transaction.date)
#         return table

#     def __repr__(self):
#         return repr_rich(self)
