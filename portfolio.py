import csv
import yfinance as yf
from rich.table import Table
from rich.panel import Panel
from rich import box
from richtools import repr_rich
from asset import Asset, Stock, ETF, Bond, Crypto
from transaction import Transaction
from typing import List, Dict

class Portfolio:
    def __init__(self, assets: Dict[str, Asset], transactions: List[Transaction]):
        self.assets: Dict[str, Asset] = assets
        self.transactions: List[Transaction] = transactions

        print(self.assets)


    def add_transaction(self, transaction):
        if transaction.asset.name not in self.assets:
            self.assets[transaction.asset.name] = transaction.asset
        if transaction.type == 'buy':
            self.assets[transaction.asset.name].amount += transaction.amount
            self.assets[transaction.asset.name].total_invested += transaction.amount * transaction.price + transaction.asset.transaction_cost
        elif transaction.type == 'sell':
            self.assets[transaction.asset.name].amount -= transaction.amount
            self.assets[transaction.asset.name].total_invested -= transaction.amount * transaction.price + transaction.asset.transaction_cost
        self.transactions.append(transaction)

    @classmethod
    def from_transactions(cls, csv_file):
        assets = {}
        transactions = []
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, type, amount, price, date = row
                asset_type = cls.identify_asset_type(name)
                asset = asset_type(name=name)
                transaction = Transaction(asset, type, float(amount), float(price), date)
                
                if asset.name not in assets:
                    assets[asset.name] = asset
                if transaction.type == 'buy':
                    assets[asset.name].amount += transaction.amount
                    assets[asset.name].total_invested += transaction.amount * transaction.price + asset.transaction_cost
                elif transaction.type == 'sell':
                    assets[asset.name].amount -= transaction.amount
                    assets[asset.name].total_invested -= transaction.amount * transaction.price + asset.transaction_cost    
                
                transactions.append(transaction)
        
        return cls(assets, transactions)
    

    def save_transactions(self, csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for transaction in self.transactions:
                writer.writerow(transaction.to_csv_row())

    def fetch_prices(self):
        for asset_name, asset in self.assets.items():
            data = yf.Ticker(asset_name).history(period='1d')
            price = data['Close'].iloc[-1]
            yield asset_name, price

    def calculate_performance(self):
        performance = {}
        for asset_name, asset in self.assets.items():
            price = next(price for a, price in self.fetch_prices() if a == asset_name)
            performance[asset_name] = asset.calculate_performance(price)
        return performance

    

    def display_performance(self):
        table = Table(title="Performance", box=box.SIMPLE, show_lines=True)

        table.add_column("Asset", justify="right", style="cyan", no_wrap=True)
        table.add_column("Initial Value", justify="right", style="yellow")
        table.add_column("Current Value", justify="right", style="green")
        table.add_column("Profit/Loss", justify="right", style="red")
        table.add_column("Profit/Loss %", justify="right", style="blue")

        performance = self.calculate_performance()
        for asset_name, data in performance.items():
            table.add_row(
                asset_name,
                f"${self.assets[asset_name].total_invested:.2f}",
                f"${data['current_value']:.2f}",
                f"${data['profit_loss']:.2f}",
                f"{data['profit_loss_percentage']:.2f}%"
            )

        print(repr_rich(Panel(table)))


    def __rich__(self):
        table = Table(title="Portfolio", box=box.SIMPLE, show_lines=True)

        table.add_column("Asset", justify="right", style="cyan", no_wrap=True)
        table.add_column("Amount", style="magenta")
        table.add_column("Current Value", justify="right", style="green")

        performance = self.calculate_performance()
        for asset_name, data in performance.items():
            table.add_row(
                asset_name,
                str(self.assets[asset_name].amount),
                f"${data['current_value']:.2f}"
            )
        return Panel(table)
    
    def __repr__(self):
        return repr_rich(self.__rich__())
    
    def display_portfolio(self):
        print(repr_rich(self.__rich__()))


    @staticmethod
    def identify_asset_type(name):
        if name.startswith("BTC") or name.startswith("ETH"):
            return Crypto
        elif "Bond" in name:
            return Bond
        elif "ETF" in name:
            return ETF
        else:
            return Stock
