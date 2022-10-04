# pylint: disable=redefined-outer-name,unused-variable

import os
from datetime import datetime

import pytest

from tinkoff.invest import (
    Account,
    Client,
    CloseSandboxAccountResponse,
    MoneyValue,
    OperationState,
    OrderDirection,
    OrderType,
    Quotation,
)


@pytest.fixture()
def sandbox_service():
    with Client(token=os.environ["INVEST_SANDBOX_TOKEN"]) as client:
        yield client.sandbox


@pytest.fixture()
def account_id(sandbox_service):
    response = sandbox_service.open_sandbox_account()
    yield response.account_id
    sandbox_service.close_sandbox_account(
        account_id=response.account_id,
    )


@pytest.fixture()
def limit_order(account_id):
    return {
        "figi": "BBG333333333",
        "quantity": 10,
        "price": Quotation(units=10),
        "direction": OrderDirection.ORDER_DIRECTION_BUY,
        "account_id": account_id,
        "order_type": OrderType.ORDER_TYPE_LIMIT,
        "order_id": "42",
    }


@pytest.fixture()
def market_order(account_id):
    return {
        "figi": "BBG333333333",
        "quantity": 10,
        "price": Quotation(units=10),
        "direction": OrderDirection.ORDER_DIRECTION_BUY,
        "account_id": account_id,
        "order_type": OrderType.ORDER_TYPE_MARKET,
        "order_id": "42",
    }


@pytest.mark.skipif(
    os.environ.get("INVEST_SANDBOX_TOKEN") is None,
    reason="Run locally with INVEST_SANDBOX_TOKEN specified",
)
class TestSandboxOperations:
    def test_open_sandbox_account(self, sandbox_service):
        response = sandbox_service.open_sandbox_account()
        assert isinstance(response.account_id, str)
        sandbox_service.close_sandbox_account(
            account_id=response.account_id,
        )

    def test_get_sandbox_accounts(self, sandbox_service, account_id):
        response = sandbox_service.get_sandbox_accounts()
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
        response = sandbox_service.open_sandbox_account()
        response = sandbox_service.close_sandbox_account(
            account_id=response.account_id,
        )
        assert isinstance(response, CloseSandboxAccountResponse)

    def test_post_sandbox_order(self, sandbox_service, limit_order):

        response = sandbox_service.post_sandbox_order(**limit_order)
        assert isinstance(response.order_id, str)
        assert response.figi == limit_order["figi"]
        assert response.direction == limit_order["direction"]
        assert response.lots_requested == limit_order["quantity"]

    def test_get_sandbox_orders(self, sandbox_service, limit_order, account_id):
        _ = sandbox_service.post_sandbox_order(**limit_order)
        response = sandbox_service.get_sandbox_orders(
            account_id=account_id,
        )
        assert isinstance(response.orders, list)
        assert len(response.orders) == 1

    def test_cancel_sandbox_order(self, sandbox_service, limit_order, account_id):
        response = sandbox_service.post_sandbox_order(**limit_order)
        response = sandbox_service.cancel_sandbox_order(
            account_id=account_id,
            order_id=response.order_id,
        )
        assert isinstance(response.time, datetime)

    def test_get_sandbox_order_state(self, sandbox_service, limit_order, account_id):
        response = sandbox_service.post_sandbox_order(**limit_order)

        response = sandbox_service.get_sandbox_order_state(
            account_id=account_id,
            order_id=response.order_id,
        )
        assert response.figi == limit_order["figi"]
        assert response.direction == limit_order["direction"]
        assert response.lots_requested == limit_order["quantity"]

    def test_get_sandbox_positions(self, sandbox_service, account_id, market_order):
        _ = sandbox_service.post_sandbox_order(**market_order)

        response = sandbox_service.get_sandbox_positions(
            account_id=account_id,
        )
        print(f">>> {response=}")

        orders = sandbox_service.get_sandbox_orders(
            account_id=account_id,
        )
        print(f">>> {orders=}")
        assert isinstance(response.money[0], MoneyValue)
        assert response.money[0].currency == "rub"

    def test_get_sandbox_operations(self, sandbox_service, account_id, limit_order):
        response = sandbox_service.get_sandbox_operations(
            account_id=account_id,
            from_=datetime(1970, 1, 1),
            to=datetime(2050, 1, 1),
            state=OperationState.OPERATION_STATE_EXECUTED,
            figi=limit_order["figi"],
        )
        assert isinstance(response.operations, list)

    def test_get_sandbox_portfolio(self, sandbox_service, account_id):
        response = sandbox_service.get_sandbox_portfolio(
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
        response = sandbox_service.sandbox_pay_in(
            account_id=account_id,
            amount=MoneyValue(currency="RUB", units=units_to_add, nano=nano_to_add),
        )
        assert response.balance.units == units_to_add
