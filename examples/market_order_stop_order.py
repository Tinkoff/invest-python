"""
Алгоритм:

выставляем рыночный ордер по дешевой бумаге
если он не исполнен - возвращаем ошибку (код и message)
если он исполнен и вернулся его идентификатор,
то выставляем тейпрофит на цену +5% к цене покупки
и стоплосс на -2% к цене покупки.
Контур выбираем: песочница или боевой.

Примеры дешевых акций:
BBG001M2SC01 84.120000000р
BBG000K3STR7 134.900000000р
BBG00F9XX7H4 142.000000000р
"""

import logging
import os
import uuid

from tinkoff.invest import (
    Client,
    OrderDirection,
    OrderExecutionReportStatus,
    OrderType,
    PostOrderResponse,
    StopOrderDirection,
    StopOrderType,
)
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.utils import decimal_to_quotation, money_to_decimal

TOKEN = os.environ["INVEST_TOKEN"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


QUANTITY = 1
INSTRUMENT_ID = "BBG001M2SC01"
USE_SANDBOX = True
TAKE_PROFIT_PERCENTAGE = 0.05
STOP_LOSS_PERCENTAGE = -0.02


def post_stop_orders(
    client: Client,
):
    pass


def main():
    if USE_SANDBOX:
        logger.info("Using Sandbox market")
        client_cls = SandboxClient
    else:
        logger.info("Using Real market")
        client_cls = Client

    with client_cls(TOKEN) as client:
        response = client.users.get_accounts()
        account, *_ = response.accounts
        account_id = account.id

        order_id = uuid.uuid4().hex

        logger.info(
            "Placing order for %s security of %s, with order_id=%s",
            QUANTITY,
            INSTRUMENT_ID,
            order_id,
        )
        post_order_response: PostOrderResponse = client.orders.post_order(
            quantity=QUANTITY,
            direction=OrderDirection.ORDER_DIRECTION_BUY,
            account_id=account_id,
            order_type=OrderType.ORDER_TYPE_MARKET,
            order_id=uuid.uuid4().hex,
            instrument_id=order_id,
        )

        status = post_order_response.execution_report_status
        if status == OrderExecutionReportStatus.EXECUTION_REPORT_STATUS_FILL:
            logger.info("Order was fulfilled, posting stop orders.")

            executed_order_price = money_to_decimal(
                post_order_response.executed_order_price
            )
            take_profit_price = executed_order_price * (1 + TAKE_PROFIT_PERCENTAGE)
            take_profit_response = client.stop_orders.post_stop_order(
                quantity=QUANTITY,
                stop_price=decimal_to_quotation(take_profit_price),
                direction=StopOrderDirection.STOP_ORDER_DIRECTION_SELL,
                account_id=account_id,
                stop_order_type=StopOrderType.STOP_ORDER_TYPE_TAKE_PROFIT,
                instrument_id=INSTRUMENT_ID,
            )
            logger.info(
                "Take profit order was placed stop_order_id=%s. Price: %s",
                take_profit_response.stop_order_id,
                take_profit_price,
            )

            stop_loss_price = executed_order_price * (1 + STOP_LOSS_PERCENTAGE)
            take_profit_response = client.stop_orders.post_stop_order(
                quantity=QUANTITY,
                stop_price=decimal_to_quotation(stop_loss_price),
                direction=StopOrderDirection.STOP_ORDER_DIRECTION_SELL,
                account_id=account_id,
                stop_order_type=StopOrderType.STOP_ORDER_TYPE_STOP_LOSS,
                instrument_id=INSTRUMENT_ID,
            )
            logger.info(
                "Stop loss order was placed stop_order_id=%s. Price: %s",
                take_profit_response.stop_order_id,
                stop_loss_price,
            )
        else:
            logger.info(
                'Order was not fulfilled: (%s) "%s"',
                post_order_response.execution_report_status,
                post_order_response.message,
            )
            logger.info("Cancelling all orders.")
            client.cancel_all_orders(account_id=account_id)


if __name__ == "__main__":
    main()
