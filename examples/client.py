import os
import sys
import uuid

from tinkoff.invest import Client, GetAccountsResponse, Account


def main() -> int:
    try:
        token = os.environ["INVEST_TOKEN"]
    except KeyError:
        print("env INVEST_TOKEN not found")  # noqa:T001
        return 1
    with Client(token) as client:
        r: GetAccountsResponse = client.users.get_accounts()  # noqa:T001
        print('Acc res:', r)
        acc, *_ = r.accounts
        assert not _
        acc: Account = acc

        s = client.orders.get_orders(account_id=acc.id)
        print('orders: ', s)

    return 0


if __name__ == "__main__":
    sys.exit(main())
