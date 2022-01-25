import random
import uuid
from unittest.mock import call

import pytest

from tinkoff.invest import GetOrdersResponse, OrderState
from tinkoff.invest.services.caching_orders_service import CachingOrdersService
from tinkoff.invest.services.orders_service import IOrdersService
from tinkoff.invest.storages.orders_storage import IOrdersStorage


@pytest.fixture()
def orders_service(mocker) -> IOrdersService:
    return mocker.create_autospec(IOrdersService)


@pytest.fixture()
def orders_storage(mocker) -> IOrdersStorage:
    return mocker.create_autospec(IOrdersStorage)


@pytest.fixture()
def caching_orders_service(
    orders_storage: IOrdersStorage, orders_service: IOrdersService
) -> CachingOrdersService:
    return CachingOrdersService(
        orders_storage=orders_storage, orders_service=orders_service
    )


class TestCachingOrdersService:
    def test_sets_new_order(
        self,
        caching_orders_service: CachingOrdersService,
        orders_service,
        orders_storage,
    ):
        expected_order_state = OrderState()
        orders_service.get_order_state.return_value = expected_order_state

        caching_orders_service.post_order()

        orders_service.post_order.assert_called_once()
        orders_service.get_order_state.assert_called_once()
        orders_storage.set.assert_called_once_with(
            item_id=expected_order_state.order_id, new_item=expected_order_state
        )

    def test_sets_order_when_gets_order_state(
        self,
        caching_orders_service: CachingOrdersService,
        orders_service,
        orders_storage,
    ):
        expected_order_state = OrderState()
        orders_service.get_order_state.return_value = expected_order_state

        caching_orders_service.get_order_state()

        orders_service.get_order_state.assert_called_once()
        orders_storage.set.assert_called_once_with(
            item_id=expected_order_state.order_id, new_item=expected_order_state
        )

    def test_deletes_order_when_cancel(
        self,
        caching_orders_service: CachingOrdersService,
        orders_service,
        orders_storage,
    ):
        order_id = uuid.uuid4().hex

        caching_orders_service.cancel_order(order_id=order_id)

        orders_service.cancel_order.assert_called_once()
        orders_storage.delete.assert_called_once_with(item_id=order_id)

    def test_deletes_old_when_gets_actual_orders(
        self,
        caching_orders_service: CachingOrdersService,
        orders_service,
        orders_storage,
    ):
        local_orders = [OrderState(order_id=uuid.uuid4().hex) for _ in range(5)]
        server_orders = random.choices(local_orders, k=3)  # noqa: S311
        orders_storage.items.return_value = [
            (order.order_id, order) for order in local_orders
        ]
        orders_service.get_orders.return_value = GetOrdersResponse(orders=server_orders)
        orders_deleted_expected = set(local_orders) - set(server_orders)

        caching_orders_service.get_orders()

        orders_service.get_orders.assert_called_once()
        orders_storage.delete.assert_has_calls(
            [call(item_id=order.order_id) for order in orders_deleted_expected]
        )
        orders_storage.set.assert_has_calls(
            [call(item_id=order.order_id, new_item=order) for order in server_orders]
        )
