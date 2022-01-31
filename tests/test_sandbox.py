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
)

pytestmark = pytest.mark.xfail


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
def order(account_id):
    return {
        "figi": "BBG00T22WKV5",
        "quantity": 10,
        "price": 100,
        "direction": OrderDirection.ORDER_DIRECTION_BUY,
        "account_id": account_id,
        "order_type": OrderType.ORDER_TYPE_MARKET,
        "order_id": "",
    }


def test_open_sandbox_account(sandbox_service):
    response = sandbox_service.open_sandbox_account()
    assert isinstance(response.account_id, str)
    sandbox_service.close_sandbox_account(
        account_id=response.account_id,
    )


def test_get_sandbox_accounts(sandbox_service, account_id):
    response = sandbox_service.get_sandbox_accounts()
    assert isinstance(response.accounts, list)
    assert isinstance(response.accounts[0], Account)
    assert (
        len([_account for _account in response.accounts if _account.id == account_id])
        == 1
    )


def test_close_sandbox_account(sandbox_service):
    response = sandbox_service.open_sandbox_account()
    response = sandbox_service.close_sandbox_account(
        account_id=response.account_id,
    )
    assert isinstance(response, CloseSandboxAccountResponse)


def test_post_sandbox_order(sandbox_service, order):

    response = sandbox_service.post_sandbox_order(**order)
    assert isinstance(response.order_id, str)
    assert response.figi == order["figi"]
    assert response.direction == order["direction"]
    assert response.lots_requested == order["quantity"]


def test_get_sandbox_orders(sandbox_service, order):
    _ = sandbox_service.post_sandbox_order(**order)
    response = sandbox_service.get_sandbox_orders(
        account_id=order["account_id"],
    )
    assert isinstance(response.orders, list)
    assert len(response.orders) == 1


def test_cancel_sandbox_order(sandbox_service, order):
    response = sandbox_service.post_sandbox_order(**order)
    response = sandbox_service.cancel_sandbox_order(
        account_id=order["account_id"],
        order_id=response.order_id,
    )
    assert isinstance(response.time, datetime)


def test_get_sandbox_order_state(sandbox_service, order):
    response = sandbox_service.post_sandbox_order(**order)

    response = sandbox_service.get_sandbox_order_state(
        account_id=order["account_id"],
        order_id=response.order_id,
    )
    assert response.figi == order["figi"]
    assert response.direction == order["direction"]
    assert response.lots_requested == order["quantity"]


def test_get_sandbox_positions(sandbox_service, account_id, order):
    _ = sandbox_service.post_sandbox_order(**order)

    response = sandbox_service.get_sandbox_positions(
        account_id=account_id,
    )
    assert isinstance(response.money[0], MoneyValue)
    assert response.money[0].currency == "rub"


def test_get_sandbox_operations(sandbox_service, account_id, order):
    response = sandbox_service.get_sandbox_operations(
        account_id=account_id,
        from_=datetime(1970, 1, 1),
        to=datetime(2050, 1, 1),
        state=OperationState.OPERATION_STATE_EXECUTED,
        figi=order["figi"],
    )
    assert isinstance(response.operations, list)


def test_get_sandbox_portfolio(sandbox_service, account_id):
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


def test_sandbox_pay_in(sandbox_service, account_id):
    units_to_add = 10000
    nano_to_add = 100
    response = sandbox_service.sandbox_pay_in(
        account_id=account_id,
        amount=MoneyValue(currency="RUB", units=units_to_add, nano=nano_to_add),
    )
    assert response.balance.units == units_to_add
