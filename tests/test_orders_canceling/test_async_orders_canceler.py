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
from tinkoff.invest.async_orders_canceling import cancel_all_orders
from tinkoff.invest.async_services import (
    AsyncServices,
    OrdersService,
    StopOrdersService,
)
from tinkoff.invest.models import AccountId


@pytest.fixture()
def orders_service(mocker) -> OrdersService:
    return mocker.create_autospec(OrdersService)


@pytest.fixture()
def stop_orders_service(mocker) -> StopOrdersService:
    return mocker.create_autospec(StopOrdersService)


@pytest.fixture()
def async_services(
    mocker, orders_service: OrdersService, stop_orders_service: StopOrdersService
) -> AsyncServices:
    async_services = mocker.create_autospec(AsyncServices)
    async_services.orders = orders_service
    async_services.stop_orders = stop_orders_service
    return async_services


@pytest.fixture()
def account_id() -> AccountId:
    return AccountId(uuid.uuid4().hex)


class TestAsyncOrdersCanceling:
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
    async def test_cancels_all_orders(
        self,
        async_services: AsyncServices,
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

        await cancel_all_orders(async_services=async_services, account_id=account_id)

        orders_service.get_orders.assert_called_once()
        orders_service.cancel_order.assert_has_calls(
            call(account_id=account_id, order_id=order.order_id) for order in orders
        )
        stop_orders_service.get_stop_orders.assert_called_once()
        stop_orders_service.cancel_stop_order.assert_has_calls(
            call(account_id=account_id, stop_order_id=stop_order.stop_order_id)
            for stop_order in stop_orders
        )
