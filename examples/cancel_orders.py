import logging

from tinkoff.invest import Client
from tinkoff.invest.invest_token import INVEST_TOKEN
from tinkoff.invest.orders_canceling import cancel_all_orders

logger = logging.getLogger(__name__)


def main():
    with Client(INVEST_TOKEN) as client:
        logger.info("Orders: %s", client.orders.get_orders(account_id=INVEST_TOKEN))
        cancel_all_orders(services=client, account_id=INVEST_TOKEN)
        logger.info("Orders: %s", client.orders.get_orders(account_id=INVEST_TOKEN))


if __name__ == "__main__":
    main()
