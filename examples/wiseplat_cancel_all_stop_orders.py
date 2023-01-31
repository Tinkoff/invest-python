"""Example - How to cancel all stop orders."""
import logging
import os

from tinkoff.invest import Client
from tinkoff.invest.exceptions import InvestError

TOKEN = os.environ["INVEST_TOKEN"]

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    """Example - How to cancel all stop orders."""
    with Client(TOKEN) as client:
        response = client.users.get_accounts()
        account, *_ = response.accounts
        account_id = account.id

        try:
            stop_orders_response = client.stop_orders.get_stop_orders(
                account_id=account_id
            )
            logger.info("Stop Orders: %s", stop_orders_response)
            for stop_order in stop_orders_response.stop_orders:
                client.stop_orders.cancel_stop_order(
                    account_id=account_id, stop_order_id=stop_order.stop_order_id
                )
                logger.info("Stop Order: %s was canceled.", stop_order.stop_order_id)
            logger.info(
                "Orders: %s", client.stop_orders.get_stop_orders(account_id=account_id)
            )
        except InvestError as error:
            logger.error("Failed to cancel all orders. Error: %s", error)


if __name__ == "__main__":
    main()
