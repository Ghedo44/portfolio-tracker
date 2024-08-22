from typing import Dict
from .transactions import Transaction
from datetime import datetime
from .asset_classes import Asset, Equity, Crypto, ETF, Cash


from rich import box
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table, Column
from rich.text import Text

from .richtools import df_to_rich_table, repr_rich

class Portfolio:
    def __init__(self, assets: Dict[str, Asset] = {}, cash_accounts: Dict[str, Cash] = {}):
        self.assets: Dict[str, Asset] = assets
        self.cash_accounts: Dict[str, Cash] = cash_accounts  # Support multiple currencies

    def add_cash_account(self, currency: str):
        if currency not in self.cash_accounts:
            self.cash_accounts[currency] = Cash(currency)
        else:
            print(f"Cash account for {currency} already exists.")

    def deposit_cash(self, currency: str, amount: float):
        if currency in self.cash_accounts:
            self.cash_accounts[currency].deposit(amount)
        else:
            raise ValueError(f"No cash account found for {currency}. Create it first.")

    def withdraw_cash(self, currency: str, amount: float):
        if currency in self.cash_accounts:
            self.cash_accounts[currency].withdraw(amount)
        else:
            raise ValueError(f"No cash account found for {currency}. Create it first.")

    def add_asset(self, asset: Asset):
        """
        Add an asset to the portfolio, without considering the cost.
        """
        self.assets[asset.symbol] = asset

    def remove_asset(self, symbol: str):
        if symbol in self.assets:
            del self.assets[symbol]
            
    def buy_asset(self, symbol: str, asset: Asset, price: float, quantity: float, currency: str = "USD"):
        total_cost = price * quantity
        if currency in self.cash_accounts and self.cash_accounts[currency].balance >= total_cost:
            # Deduct cash and add the asset to the portfolio
            self.cash_accounts[currency].withdraw(total_cost)
            if symbol in self.assets:
                self.assets[symbol].quantity += quantity
            else:
                self.assets[symbol] = asset
        else:
            raise ValueError("Insufficient cash to buy asset.")

    def sell_asset(self, symbol: str, price: float, quantity: float, currency: str = "USD"):
        if symbol in self.assets and self.assets[symbol].quantity >= quantity:
            # Sell the asset and credit the cash account
            self.assets[symbol].quantity -= quantity
            total_proceeds = price * quantity
            self.cash_accounts[currency].deposit(total_proceeds)
            if self.assets[symbol].quantity == 0:
                del self.assets[symbol]
        else:
            raise ValueError("Insufficient holdings to sell asset.")

    def update_prices(self):
        for asset in self.assets.values():
            asset.update_price()

    def add_transaction(self, symbol: str, transaction: Transaction):
        if symbol in self.assets:
            self.assets[symbol].add_transaction(transaction)

    def calculate_total_value(self):
        # Include cash balance in the total portfolio value
        total_value = sum(asset.calculate_value() for asset in self.assets.values())
        total_cash = sum(cash_account.balance for cash_account in self.cash_accounts.values())
        return total_value + total_cash

    def generate_report(self):
        # Generate a report including cash and asset holdings
        for currency, cash_account in self.cash_accounts.items():
            print(f"Cash Balance in {currency}: {cash_account.balance:.2f}")
        print(f"Total Portfolio Value: {self.calculate_total_value():.2f}")

    
    @classmethod
    def from_csv(cls, filename: str):
        """
        Create a Portfolio instance from a CSV file.
        
        The CSV file should have the following format:
        symbol, quantity, price, currency, asset_type, expense_ratio
        None,None,100000,EUR,CASH,None
        AAPL,10,150,USD,EQUITY,None
        VOO,5,400,EUR,ETF,0.03
        ...
        
        Parameters:
        filename (str): The path to the CSV file
        
        Returns:
        Portfolio: A Portfolio instance with assets loaded from the CSV file
        """
        import csv
        assets = {}
        cash_accounts = {}
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                symbol, quantity, price, currency, asset_type, expense_ratio = row
                match asset_type:
                    case "CASH":
                        if currency is None:
                            raise ValueError("Currency must be specified for cash accounts.")
                        cash_account = Cash(currency)
                        if currency not in cash_accounts:
                            cash_accounts[currency] = cash_account
                        cash_accounts[currency].deposit(float(price))                        
                        continue
                    case "EQUITY":
                        if currency is None or quantity is None or price is None:
                            raise ValueError("Currency, quantity, and price must be specified for equities.")
                        asset = Equity(symbol, float(quantity), float(price))
                    case "ETF":
                        if currency is None or quantity is None or price is None or expense_ratio is None:
                            raise ValueError("Currency, quantity, price and expense_ratio must be specified for equities.")
                        asset = ETF(symbol, float(quantity), float(price), float(expense_ratio))
                    case "CRYPTO":
                        asset = Crypto(symbol, float(quantity))
                    case _:
                        raise ValueError(f"Invalid asset type: {asset_type}")
                assets[symbol] = asset
        return cls(assets)
    
    def __rich__(self):
        equities_table = Table(title="Equities", box=box.SIMPLE, show_lines=True, min_width=60)
        equities_table.add_column("Symbol", style="cyan", no_wrap=True)
        equities_table.add_column("Quantity", style="magenta")
        equities_table.add_column("Price", style="green")
        equities_table.add_column("Value", style="blue")
        
        etfs_table = Table(title="ETFs", box=box.SIMPLE, show_lines=True, min_width=60)
        etfs_table.add_column("Symbol", style="cyan", no_wrap=True)
        etfs_table.add_column("Quantity", style="magenta")
        etfs_table.add_column("Price", style="green")
        etfs_table.add_column("Value", style="blue")
        etfs_table.add_column("Expense Ratio", style="yellow")
        
        for asset in self.assets.values():
            match type(asset).__name__:
                case 'Equity':
                    equities_table.add_row(
                        asset.symbol,
                        str(asset.quantity),
                        f"${asset.price:.2f}",
                        f"${asset.calculate_value():.2f}"
                    )
                case 'ETF':
                    etfs_table.add_row(
                        asset.symbol,
                        str(asset.quantity),
                        f"${asset.price:.2f}",
                        f"${asset.calculate_value():.2f}",
                        f"{asset.expense_ratio:.2f}%",
                    )
            
        cash_table = Table(title="Cash Accounts", box=box.SIMPLE, show_lines=True, min_width=60)
        cash_table.add_column("Currency", style="cyan", no_wrap=True)
        cash_table.add_column("Balance", style="magenta")
        for currency, cash_account in self.cash_accounts.items():
            cash_table.add_row(currency, f"${cash_account.balance:.2f}")
        return Panel(Group(equities_table, etfs_table, cash_table), title="Portfolio Summary")

    def __repr__(self):
        return repr_rich(self.__rich__())
