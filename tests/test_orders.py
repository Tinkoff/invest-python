# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import OrdersService


@pytest.fixture()
def orders_service():
    return mock.create_autospec(spec=OrdersService)


def test_post_order(orders_service):
    response = orders_service.post_order(  # noqa: F841
        figi=mock.Mock(),
        quantity=mock.Mock(),
        price=mock.Mock(),
        direction=mock.Mock(),
        account_id=mock.Mock(),
        order_type=mock.Mock(),
        order_id=mock.Mock(),
    )
    orders_service.post_order.assert_called_once()


def test_cancel_order(orders_service):
    response = orders_service.cancel_order(  # noqa: F841
        account_id=mock.Mock(),
        order_id=mock.Mock(),
    )
    orders_service.cancel_order.assert_called_once()


def test_get_order_state(orders_service):
    response = orders_service.get_order_state(  # noqa: F841
        account_id=mock.Mock(),
        order_id=mock.Mock(),
    )
    orders_service.get_order_state.assert_called_once()


def test_get_orders(orders_service):
    response = orders_service.get_orders(  # noqa: F841
        account_id=mock.Mock(),
    )
    orders_service.get_orders.assert_called_once()
