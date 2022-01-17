# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

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
