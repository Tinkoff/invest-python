import logging

from tinkoff.invest import Client
from tinkoff.invest.orders_canceling import cancel_all_orders
from tinkoff.invest.token import TOKEN

logger = logging.getLogger(__name__)


def main():
    with Client(TOKEN) as client:
        logger.info("Orders: %s", client.orders.get_orders(account_id=TOKEN))
        cancel_all_orders(services=client, account_id=TOKEN)
        logger.info("Orders: %s", client.orders.get_orders(account_id=TOKEN))


if __name__ == "__main__":
    main()
