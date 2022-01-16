# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import SandboxService


@pytest.fixture()
def sandbox_service():
    return mock.create_autospec(spec=SandboxService)


def test_open_sandbox_account(sandbox_service):
    response = sandbox_service.open_sandbox_account()  # noqa: F841
    sandbox_service.open_sandbox_account.assert_called_once()


def test_get_sandbox_accounts(sandbox_service):
    response = sandbox_service.get_sandbox_accounts()  # noqa: F841
    sandbox_service.get_sandbox_accounts.assert_called_once()


def test_close_sandbox_account(sandbox_service):
    response = sandbox_service.close_sandbox_account(  # noqa: F841
        account_id=mock.Mock(),
    )
    sandbox_service.close_sandbox_account.assert_called_once()


def test_post_sandbox_order(sandbox_service):
    response = sandbox_service.post_sandbox_order(  # noqa: F841
        figi=mock.Mock(),
        quantity=mock.Mock(),
        price=mock.Mock(),
        direction=mock.Mock(),
        account_id=mock.Mock(),
        order_type=mock.Mock(),
        order_id=mock.Mock(),
    )
    sandbox_service.post_sandbox_order.assert_called_once()


def test_get_sandbox_orders(sandbox_service):
    response = sandbox_service.get_sandbox_orders(  # noqa: F841
        account_id=mock.Mock(),
    )
    sandbox_service.get_sandbox_orders.assert_called_once()


def test_cancel_sandbox_order(sandbox_service):
    response = sandbox_service.cancel_sandbox_order(  # noqa: F841
        account_id=mock.Mock(),
        order_id=mock.Mock(),
    )
    sandbox_service.cancel_sandbox_order.assert_called_once()


def test_get_sandbox_order_state(sandbox_service):
    response = sandbox_service.get_sandbox_order_state(  # noqa: F841
        account_id=mock.Mock(),
        order_id=mock.Mock(),
    )
    sandbox_service.get_sandbox_order_state.assert_called_once()


def test_get_sandbox_positions(sandbox_service):
    response = sandbox_service.get_sandbox_positions(  # noqa: F841
        account_id=mock.Mock(),
    )
    sandbox_service.get_sandbox_positions.assert_called_once()


def test_get_sandbox_operations(sandbox_service):
    response = sandbox_service.get_sandbox_operations(  # noqa: F841
        account_id=mock.Mock(),
        from_=mock.Mock(),
        to=mock.Mock(),
        state=mock.Mock(),
        figi=mock.Mock(),
    )
    sandbox_service.get_sandbox_operations.assert_called_once()


def test_get_sandbox_portfolio(sandbox_service):
    response = sandbox_service.get_sandbox_portfolio(  # noqa: F841
        account_id=mock.Mock(),
    )
    sandbox_service.get_sandbox_portfolio.assert_called_once()


def test_sandbox_pay_in(sandbox_service):
    response = sandbox_service.sandbox_pay_in(  # noqa: F841
        account_id=mock.Mock(),
        amount=mock.Mock(),
    )
    sandbox_service.sandbox_pay_in.assert_called_once()
