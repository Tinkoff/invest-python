# pylint: disable=redefined-outer-name,unused-variable
# pylint: disable=protected-access
from unittest import mock

import pytest
from google.protobuf.json_format import MessageToDict

from tinkoff.invest._grpc_helpers import dataclass_to_protobuff
from tinkoff.invest.grpc import marketdata_pb2
from tinkoff.invest.schemas import GetMySubscriptions, MarketDataRequest
from tinkoff.invest.services import MarketDataService


@pytest.fixture()
def market_data_service():
    return mock.create_autospec(spec=MarketDataService)


def test_get_candles(market_data_service):
    response = market_data_service.get_candles(  # noqa: F841
        figi=mock.Mock(),
        from_=mock.Mock(),
        to=mock.Mock(),
        interval=mock.Mock(),
    )
    market_data_service.get_candles.assert_called_once()


def test_get_last_prices(market_data_service):
    response = market_data_service.get_last_prices(figi=mock.Mock())  # noqa: F841
    market_data_service.get_last_prices.assert_called_once()


def test_get_order_book(market_data_service):
    response = market_data_service.get_order_book(  # noqa: F841
        figi=mock.Mock(), depth=mock.Mock()
    )
    market_data_service.get_order_book.assert_called_once()


def test_get_trading_status(market_data_service):
    response = market_data_service.get_trading_status(figi=mock.Mock())  # noqa: F841
    market_data_service.get_trading_status.assert_called_once()


def test_market_data_request_get_my_subscriptions():
    expected = marketdata_pb2.MarketDataRequest(
        get_my_subscriptions=marketdata_pb2.GetMySubscriptions()
    )

    result = dataclass_to_protobuff(
        MarketDataRequest(get_my_subscriptions=GetMySubscriptions()),
        marketdata_pb2.MarketDataRequest(),
    )

    assert MessageToDict(result) == MessageToDict(expected)
