from pt import Portfolio, Equity, Transaction, ETF
from datetime import datetime

# Example Usage
portfolio = Portfolio()
apple_stock = Equity(symbol="AAPL", quantity=10, price=150)
etf = ETF(symbol="VOO", quantity=5, price=400, expense_ratio=0.03)

portfolio.add_asset(apple_stock)
portfolio.add_asset(etf)

print(portfolio)

# portfolio.add_transaction("AAPL", Transaction(apple_stock, "BUY", 10, 150, datetime.now()))

# # Fetch latest prices and update portfolio
# portfolio.update_prices()
# print(f"Total Portfolio Value: {portfolio.calculate_total_value()}")