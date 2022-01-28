import uuid
from typing import List
from unittest.mock import call

import pytest

from tinkoff.invest import (
    GetOrdersResponse,
    GetStopOrdersResponse,
    OrderState,
    StopOrder,
)
from tinkoff.invest.models import AccountId
from tinkoff.invest.orders_canceling import OrdersCanceler
from tinkoff.invest.services import OrdersService, StopOrdersService


@pytest.fixture()
def orders_service(mocker) -> OrdersService:
    return mocker.create_autospec(OrdersService)


@pytest.fixture()
def stop_orders_service(mocker) -> StopOrdersService:
    return mocker.create_autospec(StopOrdersService)


@pytest.fixture()
def account_id() -> AccountId:
    return AccountId(uuid.uuid4().hex)


@pytest.fixture()
def orders_canceler(
    orders_service: OrdersService,
    stop_orders_service: StopOrdersService,
    account_id: AccountId,
) -> OrdersCanceler:
    return OrdersCanceler(
        orders_service=orders_service,
        stop_orders_service=stop_orders_service,
        account_id=account_id,
    )


class TestOrdersCanceler:
    @pytest.mark.parametrize(
        "orders",
        [
            [
                OrderState(order_id=uuid.uuid4().hex),
                OrderState(order_id=uuid.uuid4().hex),
                OrderState(order_id=uuid.uuid4().hex),
            ],
            [OrderState(order_id=uuid.uuid4().hex)],
            [],
        ],
    )
    @pytest.mark.parametrize(
        "stop_orders",
        [
            [
                StopOrder(stop_order_id=uuid.uuid4().hex),
                StopOrder(stop_order_id=uuid.uuid4().hex),
                StopOrder(stop_order_id=uuid.uuid4().hex),
            ],
            [
                StopOrder(stop_order_id=uuid.uuid4().hex),
            ],
            [],
        ],
    )
    def test_cancels_all_orders(
        self,
        orders_canceler: OrdersCanceler,
        orders_service: OrdersService,
        stop_orders_service: StopOrdersService,
        account_id: AccountId,
        orders: List[OrderState],
        stop_orders: List[StopOrder],
    ):
        orders_service.get_orders.return_value = GetOrdersResponse(orders=orders)
        stop_orders_service.get_stop_orders.return_value = GetStopOrdersResponse(
            stop_orders=stop_orders
        )

        orders_canceler.cancel_all()

        orders_service.get_orders.assert_called_once()
        orders_service.cancel_order.assert_has_calls(
            call(account_id=account_id, order_id=order.order_id) for order in orders
        )
        stop_orders_service.get_stop_orders.assert_called_once()
        stop_orders_service.cancel_stop_order.assert_has_calls(
            call(account_id=account_id, stop_order_id=stop_order.stop_order_id)
            for stop_order in stop_orders
        )
