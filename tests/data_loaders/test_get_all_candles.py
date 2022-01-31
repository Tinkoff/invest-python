# pylint:disable=redefined-outer-name
# pylint:disable=too-many-arguments
from datetime import datetime, timedelta

import pytest

from tinkoff.invest.schemas import (
    CandleInterval,
    GetCandlesResponse,
    HistoricCandle,
    Quotation,
)
from tinkoff.invest.services import MarketDataService, Services


@pytest.fixture()
def figi():
    return "figi"


@pytest.fixture()
def from_():
    return datetime.utcnow() - timedelta(days=31)


@pytest.fixture()
def to():
    return datetime.utcnow()


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
def candles_response(historical_candle):
    return GetCandlesResponse(candles=[historical_candle])


@pytest.fixture()
def market_data_service(mocker):
    return mocker.Mock(spec=MarketDataService)


@pytest.mark.parametrize(
    ("interval", "call_count"),
    [
        (CandleInterval.CANDLE_INTERVAL_1_MIN, 32),
        (CandleInterval.CANDLE_INTERVAL_5_MIN, 32),
        (CandleInterval.CANDLE_INTERVAL_15_MIN, 32),
        (CandleInterval.CANDLE_INTERVAL_HOUR, 5),
        (CandleInterval.CANDLE_INTERVAL_DAY, 1),
    ],
)
def test_get_all_candles(
    figi, mocker, market_data_service, from_, to, candles_response, interval, call_count
):
    services = mocker.Mock()
    services.market_data = market_data_service
    market_data_service.get_candles.return_value = candles_response

    result = list(
        Services.get_all_candles(
            services,
            figi=figi,
            interval=interval,
            from_=from_,
            to=to,
        )
    )

    assert result == candles_response.candles * call_count
    assert market_data_service.get_candles.call_count == call_count
