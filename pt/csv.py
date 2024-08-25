from .transactions import Transaction
from typing import List
from csv import reader

def find_portfolio_files() -> List[str]:
    """
    Find all the csv files in the portfolio directory that starts with 'portfolio_'
    """
    from os import listdir
    from os.path import isfile, join
    mypath = "portfolio"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return [f for f in files if f.startswith("portfolio_") and f.endswith(".csv")]

def read_transactions(filename: str) -> List[Transaction]:
    """
    Read the csv with the transactions
    """
    transactions = []
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            asset = row[0]
            action = row[1]
            quantity = float(row[2])
            price = float(row[3])
            date = row[4]
            transactions.append(Transaction(asset, action, quantity, price, date))
    return transactions
    

