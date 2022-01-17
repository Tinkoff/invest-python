# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import StopOrdersService


@pytest.fixture()
def stop_orders_service():
    return mock.create_autospec(spec=StopOrdersService)


def test_post_stop_order(stop_orders_service):
    response = stop_orders_service.post_stop_order(  # noqa: F841
        figi=mock.Mock(),
        quantity=mock.Mock(),
        price=mock.Mock(),
        stop_price=mock.Mock(),
        direction=mock.Mock(),
        account_id=mock.Mock(),
        expiration_type=mock.Mock(),
        stop_order_type=mock.Mock(),
        expire_date=mock.Mock(),
    )
    stop_orders_service.post_stop_order.assert_called_once()


def test_get_stop_orders(stop_orders_service):
    response = stop_orders_service.get_stop_orders(  # noqa: F841
        account_id=mock.Mock(),
    )
    stop_orders_service.get_stop_orders.assert_called_once()


def test_cancel_stop_order(stop_orders_service):
    response = stop_orders_service.cancel_stop_order(  # noqa: F841
        account_id=mock.Mock(),
        stop_order_id=mock.Mock(),
    )
    stop_orders_service.cancel_stop_order.assert_called_once()
