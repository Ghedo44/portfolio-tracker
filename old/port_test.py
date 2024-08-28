import csv
import yfinance as yf
from rich.table import Table
from rich.console import Console
from datetime import datetime

# Define a class for each transaction
class Transaction:
    def __init__(self, asset, type, amount, price, date=None):
        self.asset = asset
        self.type = type  # 'buy' or 'sell'
        self.amount = amount
        self.price = price
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_csv_row(self):
        return [self.asset, self.type, self.amount, self.price, self.date]

# Define a class for the portfolio
class Portfolio:
    def __init__(self):
        self.assets = {}
        self.transactions = []

    def add_transaction(self, transaction):
        if transaction.asset not in self.assets:
            self.assets[transaction.asset] = 0
        if transaction.type == 'buy':
            self.assets[transaction.asset] += transaction.amount
        elif transaction.type == 'sell':
            self.assets[transaction.asset] -= transaction.amount
        self.transactions.append(transaction)

    def load_transactions(self, csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                asset, type, amount, price, date = row
                transaction = Transaction(asset, type, float(amount), float(price), date)
                self.add_transaction(transaction)

    def save_transactions(self, csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for transaction in self.transactions:
                writer.writerow(transaction.to_csv_row())

    def fetch_prices(self):
        for asset in self.assets.keys():
            data = yf.Ticker(asset).history(period='1d')
            price = data['Close'].iloc[-1]
            yield asset, price

    def calculate_performance(self):
        performance = {}
        for asset, current_amount in self.assets.items():
            price = next(price for a, price in self.fetch_prices() if a == asset)
            initial_value = sum(
                t.price * t.amount for t in self.transactions if t.asset == asset and t.type == 'buy'
            )
            current_value = price * current_amount
            performance[asset] = {
                'initial_value': initial_value,
                'current_value': current_value,
                'profit_loss': current_value - initial_value,
                'profit_loss_percentage': ((current_value - initial_value) / initial_value) * 100 if initial_value > 0 else 0,
            }
        return performance

    def display_portfolio(self):
        console = Console()
        table = Table(title="Portfolio")

        table.add_column("Asset", justify="right", style="cyan", no_wrap=True)
        table.add_column("Amount", style="magenta")
        table.add_column("Current Value", justify="right", style="green")

        performance = self.calculate_performance()
        for asset, data in performance.items():
            table.add_row(
                asset,
                str(self.assets[asset]),
                f"${data['current_value']:.2f}"
            )

        console.print(table)

    def display_performance(self):
        console = Console()
        table = Table(title="Performance")

        table.add_column("Asset", justify="right", style="cyan", no_wrap=True)
        table.add_column("Initial Value", justify="right", style="yellow")
        table.add_column("Current Value", justify="right", style="green")
        table.add_column("Profit/Loss", justify="right", style="red")
        table.add_column("Profit/Loss %", justify="right", style="blue")

        performance = self.calculate_performance()
        for asset, data in performance.items():
            table.add_row(
                asset,
                f"${data['initial_value']:.2f}",
                f"${data['current_value']:.2f}",
                f"${data['profit_loss']:.2f}",
                f"{data['profit_loss_percentage']:.2f}%"
            )

        console.print(table)


# Example usage
if __name__ == "__main__":
    portfolio = Portfolio()

    # Load existing transactions
    portfolio.load_transactions("portfolio_transactions.csv")

    # Add a new transaction
    transaction = Transaction(asset="AAPL", type="buy", amount=10, price=150)
    portfolio.add_transaction(transaction)

    # Save transactions
    portfolio.save_transactions("portfolio_transactions.csv")

    # Display portfolio and performance
    portfolio.display_portfolio()
    portfolio.display_performance()
