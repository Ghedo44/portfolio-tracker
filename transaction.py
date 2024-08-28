from datetime import datetime

class Transaction:
    def __init__(self, asset, type, amount, price, date=None):
        self.asset = asset
        self.type = type  # 'buy' or 'sell'
        self.amount = amount
        self.price = price
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_csv_row(self):
        return [self.asset.name, self.type, self.amount, self.price, self.date]
