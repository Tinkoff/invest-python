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
from tinkoff.invest.services import OrdersService, Services, StopOrdersService
from tinkoff.invest.typedefs import AccountId


@pytest.fixture()
def orders_service(mocker) -> OrdersService:
    return mocker.create_autospec(OrdersService)


@pytest.fixture()
def stop_orders_service(mocker) -> StopOrdersService:
    return mocker.create_autospec(StopOrdersService)


@pytest.fixture()
def services(
    mocker, orders_service: OrdersService, stop_orders_service: StopOrdersService
) -> Services:
    services = mocker.create_autospec(Services)
    services.orders = orders_service
    services.stop_orders = stop_orders_service
    return services


@pytest.fixture()
def account_id() -> AccountId:
    return AccountId(uuid.uuid4().hex)


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
        services: Services,
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

        Services.cancel_all_orders(services, account_id=account_id)

        orders_service.get_orders.assert_called_once()
        orders_service.cancel_order.assert_has_calls(
            call(account_id=account_id, order_id=order.order_id) for order in orders
        )
        stop_orders_service.get_stop_orders.assert_called_once()
        stop_orders_service.cancel_stop_order.assert_has_calls(
            call(account_id=account_id, stop_order_id=stop_order.stop_order_id)
            for stop_order in stop_orders
        )
