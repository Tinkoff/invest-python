import logging

from tinkoff.invest import Client
from tinkoff.invest.orders_canceling import cancel_all_orders
from tinkoff.invest.token import TOKEN

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    with Client(TOKEN) as client:
        response = client.users.get_accounts()
        account, *_ = response.accounts
        account_id = account.id
        logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))
        cancel_all_orders(services=client, account_id=account.id)
        logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))


if __name__ == "__main__":
    main()
