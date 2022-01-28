import logging

from tinkoff.invest import Client
from tinkoff.invest.invest_token import INVEST_TOKEN
from tinkoff.invest.orders_canceling import OrdersCanceler

logger = logging.getLogger(__name__)


def main():
    with Client(INVEST_TOKEN) as client:
        orders_canceler = OrdersCanceler(
            orders_service=client.orders,
            stop_orders_service=client.stop_orders,
            account_id=INVEST_TOKEN,
        )
        logger.info("Orders: %s", client.orders.get_orders(account_id=INVEST_TOKEN))
        orders_canceler.cancel_all()
        logger.info("Orders: %s", client.orders.get_orders(account_id=INVEST_TOKEN))


if __name__ == "__main__":
    main()
