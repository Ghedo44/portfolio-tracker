from pt import Portfolio, Stock, ETF, Transaction, PortfolioFromCsv


portfolio: Portfolio = PortfolioFromCsv("fineco.csv")

# Example: Add a new stock transaction with dividends
stock = Stock(name="AAPL", transaction_cost=10, dividends=50)
transaction = Transaction(asset=stock, type="buy", amount=10, price=150)
portfolio.add_transaction(transaction)

# Example: Add a new ETF transaction with annual cost
etf = ETF(name="SPY", transaction_cost=5, annual_cost=20)
transaction = Transaction(asset=etf, type="buy", amount=5, price=400)
portfolio.add_transaction(transaction)

# Save transactions
portfolio.save_transactions("portfolio_transactions.csv")

# Display portfolio and performance
portfolio.display_portfolio()
portfolio.display_performance()

print(portfolio.assets)
print(portfolio.transactions)
print(portfolio.transactions.first_page())
print(portfolio.transactions[-1])
