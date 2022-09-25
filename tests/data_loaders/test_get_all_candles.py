# pylint:disable=redefined-outer-name
# pylint:disable=too-many-arguments
from copy import copy
from datetime import timedelta

import pytest

from tinkoff.invest.schemas import (
    CandleInterval,
    GetCandlesResponse,
    HistoricCandle,
    Quotation,
)
from tinkoff.invest.services import MarketDataService, Services
from tinkoff.invest.utils import now


@pytest.fixture()
def figi():
    return "figi"


@pytest.fixture()
def from_():
    return now() - timedelta(days=31)


@pytest.fixture()
def to():
    return now()


@pytest.fixture()
def historical_candle():
    quotation = Quotation(units=100, nano=0)
    return HistoricCandle(
        open=quotation,
        high=quotation,
        low=quotation,
        close=quotation,
        volume=100,
        time=now(),
        is_complete=False,
    )


@pytest.fixture()
def candles_response(historical_candle):
    return GetCandlesResponse(candles=[historical_candle])


@pytest.fixture()
def market_data_service(mocker):
    return mocker.Mock(spec=MarketDataService)


class TestGetAllCandles:
    @pytest.mark.parametrize(
        ("interval", "call_count"),
        [
            (CandleInterval.CANDLE_INTERVAL_1_MIN, 31),
            (CandleInterval.CANDLE_INTERVAL_5_MIN, 31),
            (CandleInterval.CANDLE_INTERVAL_15_MIN, 31),
            (CandleInterval.CANDLE_INTERVAL_HOUR, 5),
            (CandleInterval.CANDLE_INTERVAL_DAY, 1),
        ],
    )
    @pytest.mark.parametrize("use_to", [True, False])
    def test_get_all_candles(
        self,
        figi,
        mocker,
        market_data_service,
        from_,
        to,
        candles_response,
        interval,
        call_count,
        use_to,
    ):
        services = mocker.Mock()
        services.market_data = market_data_service
        market_data_service.get_candles.return_value = candles_response

        to_kwarg = {}
        if use_to:
            to_kwarg = {"to": to}
        result = list(
            Services.get_all_candles(
                services,
                figi=figi,
                interval=interval,
                from_=from_,
                **to_kwarg,
            )
        )

        assert result == candles_response.candles * call_count
        assert market_data_service.get_candles.call_count == call_count

    @pytest.mark.parametrize(
        "interval",
        [
            *[
                interval
                for interval in CandleInterval
                if interval != CandleInterval.CANDLE_INTERVAL_UNSPECIFIED
            ],
        ],
    )
    @pytest.mark.parametrize(
        "allow_candle_duplicates",
        [
            True,
            False,
        ],
    )
    def test_deduplicates(
        self,
        figi,
        mocker,
        market_data_service,
        from_,
        to,
        candles_response,
        interval,
        historical_candle,
        allow_candle_duplicates,
    ):
        services = mocker.Mock()
        services.market_data = market_data_service

        def _get_duplicated_candle_response(*args, **kwargs):
            return GetCandlesResponse(
                candles=[copy(historical_candle) for _ in range(3)]
            )

        market_data_service.get_candles = _get_duplicated_candle_response

        candles = list(
            Services.get_all_candles(
                services,
                figi=figi,
                interval=interval,
                from_=from_,
                to=to,
                allow_candle_duplicates=allow_candle_duplicates,
            )
        )

        if allow_candle_duplicates:
            assert len(candles) > 1
        else:
            assert len(candles) == 1
