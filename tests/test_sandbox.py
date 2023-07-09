# pylint: disable=redefined-outer-name,unused-variable

import os
from datetime import datetime

import pytest

from tinkoff.invest import (
    Account,
    CloseSandboxAccountResponse,
    MoneyValue,
    OperationState,
    OrderDirection,
    OrderType,
    Quotation,
)
from tinkoff.invest.sandbox.client import SandboxClient


@pytest.fixture()
def sandbox_service():
    with SandboxClient(token=os.environ["INVEST_SANDBOX_TOKEN"]) as client:
        yield client


@pytest.fixture()
def account_id(sandbox_service):
    response = sandbox_service.sandbox.open_sandbox_account()
    yield response.account_id
    sandbox_service.sandbox.close_sandbox_account(
        account_id=response.account_id,
    )


@pytest.fixture()
def figi() -> str:
    return "BBG333333333"


@pytest.fixture()
def quantity() -> int:
    return 10


@pytest.fixture()
def price() -> Quotation:
    return Quotation(units=10, nano=0)


@pytest.fixture()
def direction() -> OrderDirection:
    return OrderDirection.ORDER_DIRECTION_BUY


@pytest.fixture()
def order_type() -> OrderType:
    return OrderType.ORDER_TYPE_LIMIT


@pytest.fixture()
def order_id() -> str:
    return ""


@pytest.fixture()
def order(figi, quantity, price, direction, account_id, order_type, order_id):
    return {
        "figi": figi,
        "quantity": quantity,
        "price": price,
        "direction": direction,
        "account_id": account_id,
        "order_type": order_type,
        "order_id": order_id,
    }


@pytest.mark.skipif(
    os.environ.get("INVEST_SANDBOX_TOKEN") is None,
    reason="INVEST_SANDBOX_TOKEN should be specified",
)
class TestSandboxOperations:
    def test_open_sandbox_account(self, sandbox_service):
        response = sandbox_service.sandbox.open_sandbox_account()
        assert isinstance(response.account_id, str)
        sandbox_service.sandbox.close_sandbox_account(
            account_id=response.account_id,
        )

    def test_get_sandbox_accounts(self, sandbox_service, account_id):
        response = sandbox_service.users.get_accounts()
        assert isinstance(response.accounts, list)
        assert isinstance(response.accounts[0], Account)
        assert (
            len(
                [
                    _account
                    for _account in response.accounts
                    if _account.id == account_id
                ]
            )
            == 1
        )

    def test_close_sandbox_account(self, sandbox_service):
        response = sandbox_service.sandbox.open_sandbox_account()
        response = sandbox_service.sandbox.close_sandbox_account(
            account_id=response.account_id,
        )
        assert isinstance(response, CloseSandboxAccountResponse)

    def test_post_sandbox_order(
        self, sandbox_service, order, figi, direction, quantity
    ):
        response = sandbox_service.orders.post_order(**order)
        assert isinstance(response.order_id, str)
        assert response.figi == figi
        assert response.direction == direction
        assert response.lots_requested == quantity

    def test_get_sandbox_orders(self, sandbox_service, order, account_id):
        _ = sandbox_service.orders.post_order(**order)
        response = sandbox_service.orders.get_orders(
            account_id=account_id,
        )
        assert isinstance(response.orders, list)
        assert len(response.orders) == 1

    def test_cancel_sandbox_order(self, sandbox_service, order, account_id):
        response = sandbox_service.orders.post_order(**order)
        response = sandbox_service.orders.cancel_order(
            account_id=account_id,
            order_id=response.order_id,
        )
        assert isinstance(response.time, datetime)

    def test_get_sandbox_order_state(
        self, sandbox_service, order, account_id, figi, direction, quantity
    ):
        response = sandbox_service.orders.post_order(**order)

        response = sandbox_service.orders.get_order_state(
            account_id=account_id,
            order_id=response.order_id,
        )
        assert response.figi == figi
        assert response.direction == direction
        assert response.lots_requested == quantity

    @pytest.mark.parametrize("order_type", [OrderType.ORDER_TYPE_MARKET])
    def test_get_sandbox_positions(self, sandbox_service, account_id, order):
        _ = sandbox_service.orders.post_order(**order)

        response = sandbox_service.operations.get_positions(account_id=account_id)

        assert isinstance(response.money[0], MoneyValue)
        assert response.money[0].currency == "rub"

    def test_get_sandbox_operations(self, sandbox_service, account_id, order, figi):
        response = sandbox_service.operations.get_operations(
            account_id=account_id,
            from_=datetime(2000, 2, 2),
            to=datetime(2022, 2, 2),
            state=OperationState.OPERATION_STATE_EXECUTED,
            figi=figi,
        )
        assert isinstance(response.operations, list)

    def test_get_sandbox_portfolio(self, sandbox_service, account_id):
        response = sandbox_service.operations.get_portfolio(
            account_id=account_id,
        )
        assert str(response.total_amount_bonds) == str(
            MoneyValue(currency="rub", units=0, nano=0)
        )
        assert str(response.total_amount_currencies) == str(
            MoneyValue(currency="rub", units=0, nano=0)
        )
        assert str(response.total_amount_etf) == str(
            MoneyValue(currency="rub", units=0, nano=0)
        )
        assert str(response.total_amount_futures) == str(
            MoneyValue(currency="rub", units=0, nano=0)
        )
        assert str(response.total_amount_shares) == str(
            MoneyValue(currency="rub", units=0, nano=0)
        )

    def test_sandbox_pay_in(self, sandbox_service, account_id):
        units_to_add = 10000
        nano_to_add = 100
        response = sandbox_service.sandbox.sandbox_pay_in(
            account_id=account_id,
            amount=MoneyValue(currency="RUB", units=units_to_add, nano=nano_to_add),
        )
        assert response.balance.units == units_to_add
