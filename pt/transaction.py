from datetime import datetime
from pt.asset import Asset

class Transaction:
    def __init__(self, asset: Asset, type: str, amount: int, price: float, date=None):
        self.asset = asset
        self.type = type  # 'buy' or 'sell'
        self.amount = amount
        self.price = price
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_csv_row(self):
        return [self.asset.name, self.type, self.amount, self.price, self.date]
