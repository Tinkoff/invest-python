import logging
import os

from tinkoff.invest import Client

TOKEN = os.environ["INVEST_TOKEN"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    with Client(TOKEN) as client:
        response = client.users.get_accounts()
        account, *_ = response.accounts
        account_id = account.id
        logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))
        client.cancel_all_orders(account_id=account.id)
        logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))


if __name__ == "__main__":
    main()
