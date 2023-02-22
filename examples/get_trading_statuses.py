import os

from tinkoff.invest import Client

token = os.environ["INVEST_TOKEN"]


with Client(token) as client:
    accounts = client.users.get_accounts()
    account_id = accounts.accounts[0].id

    statuses = client.market_data.get_trading_statuses(instrument_ids=["BBG004730N88"])
    print(statuses)
