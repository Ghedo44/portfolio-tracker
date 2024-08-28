from .asset_classes import Asset
from datetime import datetime

# type Action = "BUY" | "SELL" | "DIVIDEND" | "SPLIT"

class Transaction:
    def __init__(self, asset: Asset, action: str, quantity: float, price: float, date: datetime):
        self.asset = asset
        self.action = action  # Buy, Sell, Dividend, etc.
        self.quantity = quantity
        self.price = price
        self.date = date

    def __str__(self):
        return f"{self.action} {self.quantity} of {self.asset.symbol} at {self.price} on {self.date}"