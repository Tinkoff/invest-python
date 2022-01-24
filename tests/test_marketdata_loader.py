# pylint: disable=redefined-outer-name,unused-variable
# pylint: disable=protected-access
import math
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import MagicMock

import pytest

from tinkoff.invest import CandleInterval, GetCandlesResponse, HistoricCandle, Quotation
from tinkoff.invest.data_loaders import MarketDataLoader
from tinkoff.invest.services import MarketDataService


@pytest.fixture()
def from_date():
    return datetime(2000, 1, 1, 0, 0, 0)


@pytest.fixture()
def interval_in_days():
    return 31


@pytest.fixture()
def historical_candle():
    quotation = Quotation(units=100, nano=0)
    return HistoricCandle(
        open=quotation,
        high=quotation,
        low=quotation,
        close=quotation,
        volume=100,
        time=datetime.utcnow(),
        is_complete=False,
    )


@pytest.fixture()
def market_data_service():
    return mock.create_autospec(spec=MarketDataService)


@pytest.fixture()
def market_data_loader(
    market_data_service, historical_candle, from_date, interval_in_days
):
    to = from_date + timedelta(days=interval_in_days)
    market_data_loader = MarketDataLoader(
        service=market_data_service, from_=from_date, to=to
    )
    market_data_loader._request_candles = MagicMock(
        return_value=GetCandlesResponse(candles=[historical_candle])
    )
    return market_data_loader


@pytest.fixture()
def market_data_loader_1m_interval(market_data_loader):
    market_data_loader._interval = CandleInterval.CANDLE_INTERVAL_1_MIN
    return market_data_loader


@pytest.fixture()
def market_data_loader_1h_interval(market_data_loader):
    market_data_loader._interval = CandleInterval.CANDLE_INTERVAL_HOUR
    return market_data_loader


def test_separate_date_for_1_min_candles(
    market_data_loader_1m_interval, interval_in_days
):
    intervals = list(market_data_loader_1m_interval.separated_date_for_intervals)

    assert len(intervals) == interval_in_days
    assert intervals == sorted(intervals, key=lambda x: x[0], reverse=True)
    assert intervals == sorted(intervals, key=lambda x: x[1], reverse=True)
    assert all(interval[0] < interval[1] for interval in intervals)


def test_get_1_min_candles(
    market_data_loader_1m_interval, interval_in_days, historical_candle
):
    candles = list(market_data_loader_1m_interval)

    assert len(candles) == interval_in_days
    assert candles == [historical_candle] * interval_in_days


def test_separate_date_for_hour_candles(
    market_data_loader_1h_interval, interval_in_days
):
    intervals = list(market_data_loader_1h_interval.separated_date_for_intervals)

    assert len(intervals) == math.ceil(interval_in_days / 7)
    assert intervals == sorted(intervals, key=lambda x: x[0], reverse=True)
    assert intervals == sorted(intervals, key=lambda x: x[1], reverse=True)
    assert all(interval[0] < interval[1] for interval in intervals)


def test_get_1h_candles(
    market_data_loader_1h_interval, interval_in_days, historical_candle
):
    candles = list(market_data_loader_1h_interval)

    assert len(candles) == math.ceil(interval_in_days / 7)
    assert candles == [historical_candle] * math.ceil(interval_in_days / 7)
