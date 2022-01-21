# pylint: disable=redefined-outer-name,unused-variable
# pylint: disable=protected-access
import math
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import MagicMock

import pytest

from tinkoff.invest import CandleInterval, GetCandlesResponse, HistoricCandle, Quotation
from tinkoff.invest.service_helpers import MarketDataServiceHelper
from tinkoff.invest.services import MarketDataService


@pytest.fixture()
def figi():
    return "figi"


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
def market_data_service_helper(market_data_service, historical_candle):
    service_helper = MarketDataServiceHelper(market_data_service)
    service_helper._request_candles = MagicMock(
        return_value=GetCandlesResponse(candles=[historical_candle])
    )
    return service_helper


@pytest.fixture()
def from_date():
    return datetime(2000, 1, 1, 0, 0, 0)


@pytest.fixture()
def interval_in_days():
    return 31


def test_separate_date_for_1_min_candles(from_date, interval_in_days):
    to = from_date + timedelta(days=interval_in_days)

    intervals = list(
        MarketDataServiceHelper._separate_date_for_intervals(
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
        MarketDataServiceHelper._separate_date_for_intervals(
            from_date, to, CandleInterval.CANDLE_INTERVAL_HOUR
        )
    )

    assert len(intervals) == math.ceil(interval_in_days / 7)
    assert intervals == sorted(intervals, key=lambda x: x[0], reverse=True)
    assert intervals == sorted(intervals, key=lambda x: x[1], reverse=True)
    assert all(interval[0] < interval[1] for interval in intervals)


def test_get_candles_withoit_dates(market_data_service_helper, figi, historical_candle):
    res = list(
        market_data_service_helper.get_candles(
            figi=figi, interval=CandleInterval.CANDLE_INTERVAL_1_MIN
        )
    )

    assert res == [historical_candle]
