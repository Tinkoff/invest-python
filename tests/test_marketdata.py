# pylint: disable=redefined-outer-name,unused-variable
# pylint: disable=protected-access
import math
from datetime import datetime, timedelta
from unittest import mock

import pytest

from tinkoff.invest import CandleInterval
from tinkoff.invest.services import MarketDataService


@pytest.fixture()
def market_data_service():
    return mock.create_autospec(spec=MarketDataService)


@pytest.fixture()
def from_date():
    return datetime(2000, 1, 1, 0, 0, 0)


@pytest.fixture()
def interval_in_days():
    return 31


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


def test_separate_date_for_1_min_candles(from_date, interval_in_days):
    to = from_date + timedelta(days=interval_in_days)

    intervals = list(
        MarketDataService._separate_date_for_intervals(
            from_date, to, CandleInterval.CANDLE_INTERVAL_1_MIN
        )
    )

    assert len(intervals) == interval_in_days
    assert intervals == sorted(intervals, key=lambda x: x[0], reverse=True)
    assert intervals == sorted(intervals, key=lambda x: x[1], reverse=True)
    assert all(interval[0] < interval[1] for interval in intervals)


def test_separate_date_for_hour_candles(from_date, interval_in_days):
    to = from_date + timedelta(days=interval_in_days)

    intervals = list(
        MarketDataService._separate_date_for_intervals(
            from_date, to, CandleInterval.CANDLE_INTERVAL_HOUR
        )
    )

    assert len(intervals) == math.ceil(interval_in_days / 7)
    assert intervals == sorted(intervals, key=lambda x: x[0], reverse=True)
    assert intervals == sorted(intervals, key=lambda x: x[1], reverse=True)
    assert all(interval[0] < interval[1] for interval in intervals)
