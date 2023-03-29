""" Example - How to set/get balance for sandbox account.
    How to get/close all sandbox accounts.
    How to open new sandbox account. """

import logging
import os
from datetime import datetime
from decimal import Decimal

from tinkoff.invest import MoneyValue
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.utils import decimal_to_quotation, quotation_to_decimal

TOKEN = os.environ["INVEST_TOKEN"]

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def add_money_sandbox(client, account_id, money, currency="rub"):
    """Function to add money to sandbox account."""
    money = decimal_to_quotation(Decimal(money))
    return client.sandbox.sandbox_pay_in(
        account_id=account_id,
        amount=MoneyValue(units=money.units, nano=money.nano, currency=currency),
    )


def main():
    """Example - How to set/get balance for sandbox account.
    How to get/close all sandbox accounts.
    How to open new sandbox account."""
    with SandboxClient(TOKEN) as client:
        # get all sandbox accounts
        sandbox_accounts = client.users.get_accounts()
        print(sandbox_accounts)

        # close all sandbox accounts
        for sandbox_account in sandbox_accounts.accounts:
            client.sandbox.close_sandbox_account(account_id=sandbox_account.id)

        # open new sandbox account
        sandbox_account = client.sandbox.open_sandbox_account()
        print(sandbox_account.account_id)

        account_id = sandbox_account.account_id

        # add initial 2 000 000 to sandbox account
        print(add_money_sandbox(client=client, account_id=account_id, money=2000000))
        logger.info(
            "positions: %s", client.operations.get_positions(account_id=account_id)
        )
        print(
            "money: ",
            float(
                quotation_to_decimal(
                    client.operations.get_positions(account_id=account_id).money[0]
                )
            ),
        )

        logger.info(
            "orders: %s", client.orders.get_orders(account_id=account_id)
        )
        logger.info(
            "positions: %s", client.operations.get_positions(account_id=account_id)
        )
        logger.info(
            "portfolio: %s", client.operations.get_portfolio(account_id=account_id)
        )
        logger.info(
            "operations: %s",
            client.operations.get_operations(
                account_id=account_id,
                from_=datetime(2023, 1, 1),
                to=datetime(2023, 2, 5),
            ),
        )
        logger.info(
            "withdraw_limits: %s",
            client.operations.get_withdraw_limits(account_id=account_id),
        )

        # add + 2 000 000 to sandbox account, total is 4 000 000
        print(add_money_sandbox(client=client, account_id=account_id, money=2000000))
        logger.info(
            "positions: %s", client.operations.get_positions(account_id=account_id)
        )

        # close new sandbox account
        sandbox_account = client.sandbox.close_sandbox_account(
            account_id=sandbox_account.account_id
        )
        print(sandbox_account)


if __name__ == "__main__":
    main()
