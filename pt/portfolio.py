import csv
from rich.table import Table
from rich.panel import Panel
from rich import box
from pt.richtools import repr_rich
from pt.asset import Assets, Asset, Stock, ETF, Bond, Crypto
from pt.transaction import Transaction, Transactions

class Portfolio:
    def __init__(self, assets: Assets, transactions: Transactions):
        self.assets: Assets = assets
        self.transactions: Transactions = transactions

    def add_transaction(self, transaction: Transaction):
        if transaction.asset.name not in self.assets:
            self.assets[transaction.asset.name] = transaction.asset
        if transaction.type == 'buy':
            self.assets[transaction.asset.name].average_loading_price = self.average_loading_price(transaction.asset, transaction.amount, transaction.price)
            self.assets[transaction.asset.name].amount += transaction.amount
            self.assets[transaction.asset.name].total_invested += transaction.amount * transaction.price
        elif transaction.type == 'sell':
            self.assets[transaction.asset.name].amount -= transaction.amount
            self.assets[transaction.asset.name].total_invested -= transaction.amount * transaction.price
        self.transactions.append(transaction)

    @classmethod
    def load_transactions(cls, csv_file):
        assets = Assets()
        transactions = Transactions()
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, asset_type, currency, transaction_type, amount, price, transaction_cost, date = row
                asset: Asset = cls.identify_asset(asset_type)(name=name, currency=currency)
                transaction = Transaction(asset, transaction_type, currency, float(amount), float(price), float(transaction_cost), date)
                
                if asset.name not in assets:
                    assets[asset.name] = asset
                if transaction.type == 'buy':
                    assets[asset.name].average_loading_price = cls.average_loading_price(asset, transaction.amount, transaction.price)
                    assets[asset.name].amount += transaction.amount
                    assets[asset.name].total_invested += transaction.amount * transaction.price
                elif transaction.type == 'sell':
                    assets[asset.name].amount -= transaction.amount
                    assets[asset.name].total_invested -= transaction.amount * transaction.price    
                
                transactions.append(transaction)

        return cls(assets, transactions)
    
    def save_transactions(self, csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for transaction in self.transactions:
                writer.writerow(transaction.to_csv_row())


    def calculate_performance(self):
        return self.assets.calculate_performance()

    def display_performance(self):
        table = Table(box=box.SIMPLE, show_lines=True)

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

        print(repr_rich(Panel(table, title="Performance")))


    def __rich__(self):
        table = Table(box=box.SIMPLE, show_lines=True)

        table.add_column("Asset", justify="right", style="cyan", no_wrap=True)
        table.add_column("Amount", style="magenta")
        table.add_column("Current Value", justify="right", style="green")
        table.add_column("Total Invested", justify="right", style="blue")
        table.add_column("Profit/Loss", justify="right", style="red")
        table.add_column("Profit/Loss %", justify="right", style="blue")
        table.add_column("Price", justify="right", style="yellow")

        performance = self.calculate_performance()
        for asset_name, data in performance.items():
            table.add_row(
                asset_name,
                str(self.assets[asset_name].amount),
                f"${data['current_value']:.2f}",
                f"${self.assets[asset_name].total_invested:.2f}",
                f"${data['profit_loss']:.2f}",
                f"{data['profit_loss_percentage']:.2f}%",
                f"${self.assets[asset_name].price:.2f}"
            )
        return Panel(table, title="Portfolio Summary")
    
    def __repr__(self):
        return repr_rich(self.__rich__())
    
    def display_portfolio(self):
        print(repr_rich(self.__rich__()))


    @staticmethod
    def identify_asset(asset_type) -> Asset:
        match asset_type:
            case "Stock":
                return Stock
            case "ETF":
                return ETF
            case "Bond":
                return Bond
            case "Crypto":
                return Crypto
            case _:
                raise ValueError(f"Unknown asset type: {asset_type}")
            
    @staticmethod
    def average_loading_price(asset: Asset, amount: int, price: float) -> float:
        return (asset.average_loading_price * asset.amount + amount * price) / (asset.amount + amount)
