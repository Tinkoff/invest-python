# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import OperationsService


@pytest.fixture()
def operations_service():
    return mock.create_autospec(spec=OperationsService)


def test_get_operations(operations_service):
    response = operations_service.get_operations(  # noqa: F841
        account_id=mock.Mock(),
        from_=mock.Mock(),
        to=mock.Mock(),
        state=mock.Mock(),
        figi=mock.Mock(),
    )
    operations_service.get_operations.assert_called_once()


def test_get_portfolio(operations_service):
    response = operations_service.get_portfolio(  # noqa: F841
        account_id=mock.Mock(),
    )
    operations_service.get_portfolio.assert_called_once()


def test_get_positions(operations_service):
    response = operations_service.get_positions(  # noqa: F841
        account_id=mock.Mock(),
    )
    operations_service.get_positions.assert_called_once()


def test_get_withdraw_limits(operations_service):
    response = operations_service.get_withdraw_limits(  # noqa: F841
        account_id=mock.Mock(),
    )
    operations_service.get_withdraw_limits.assert_called_once()
