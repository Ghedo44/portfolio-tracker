from pt.portfolio import Portfolio
from pt.asset_classes import Equity

def test_portfolio():
    # Create a portfolio
    portfolio = Portfolio()
    
    # Add a cash account
    portfolio.add_cash_account("USD")
    
    # Deposit cash
    portfolio.deposit_cash("USD", 1000)
    
    print(portfolio.cash_accounts)
    assert portfolio.cash_accounts["USD"].balance == 1000
    
    # Add an asset
    asset = Equity("AAPL", 10, 150)
    portfolio.add_asset(asset)
    
    # Buy an asset
    portfolio.buy_asset("AAPL", 150, 10)
    
    # Update prices
    portfolio.update_prices()
    
    # Sell an asset
    portfolio.sell_asset("AAPL", 160, 5)
    
    # Remove an asset
    portfolio.remove_asset("AAPL")
    
    # Withdraw cash
    portfolio.withdraw_cash("USD", 500)
    
    # Check total value
    assert portfolio.calculate_total_value() == 2500