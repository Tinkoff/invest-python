import pytest

from tinkoff.invest import OrderState
from tinkoff.invest.services.caching_orders_service import CachingOrdersService
from tinkoff.invest.services.orders_service import IOrdersService
from tinkoff.invest.storages.orders_storage import IOrdersStorage


@pytest.fixture()
def orders_service(mocker) -> IOrdersService:
    return mocker.Mock(spec=IOrdersService)


@pytest.fixture()
def orders_storage(mocker) -> IOrdersStorage:
    return mocker.Mock(spec=IOrdersStorage)


@pytest.fixture()
def caching_orders_service(
    orders_storage: IOrdersStorage, orders_service: IOrdersService
) -> CachingOrdersService:
    return CachingOrdersService(
        orders_storage=orders_storage, orders_service=orders_service
    )


class TestCachingOrdersService:
    def test_adds_new_order(
        self,
        caching_orders_service: CachingOrdersService,
        orders_service: IOrdersService,
        orders_storage: IOrdersStorage,
    ):
        expected_order_state = OrderState()
        orders_service.get_order_state.return_value = expected_order_state

        caching_orders_service.post_order()

        orders_service.get_order_state.assert_called_once()
        orders_storage.set.assert_called_once_with(
            item_id=expected_order_state.order_id, new_item=expected_order_state
        )
