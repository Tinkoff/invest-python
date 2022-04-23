import logging
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pytest

from tinkoff.invest import CandleInterval, Client, GetCandlesResponse, Quotation, \
    HistoricCandle
from tinkoff.invest.caching.cache_settings import MarketDataCacheSettings
from tinkoff.invest.services import MarketDataCache, MarketDataService
from tinkoff.invest.utils import now, candle_interval_to_timedelta
import tempfile

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


def get_historical_candle(time: datetime):
    quotation = Quotation(units=100, nano=0)
    return HistoricCandle(
        open=quotation,
        high=quotation,
        low=quotation,
        close=quotation,
        volume=100,
        time=time,
        is_complete=True,
    )

def get_candles_response(start: datetime, end: datetime, interval: CandleInterval):
    delta = candle_interval_to_timedelta(interval)
    current_time = start
    times = []
    while current_time <= end:
        times.append(current_time)
        current_time += delta

    return GetCandlesResponse(candles=[get_historical_candle(time) for time in times])


@pytest.fixture()
def market_data_service(mocker) -> MarketDataService:
    service = mocker.Mock(spec=MarketDataService)
    def _get_candles(
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
    ) -> GetCandlesResponse:
        return get_candles_response(start=from_, end=to, interval=interval)
    service.get_candles = _get_candles
    service.get_candles = mocker.Mock(wraps=service.get_candles)
    return service


@pytest.fixture()
def client(mocker, market_data_service):
    with Client(mocker.Mock()) as client:
        client.market_data = market_data_service
        yield client


class TestCachedLoad:
    def test_loads_from_net(self, client):
        settings = MarketDataCacheSettings(base_cache_dir=Path(tempfile.gettempdir()))
        market_data_cache = MarketDataCache(
            settings=settings, services=client
        )

        result = list(market_data_cache.get_all_candles(
            figi=uuid.uuid4().hex,
            from_=now() - timedelta(days=30),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ))

        assert result

    def test_loads_from_net_then_from_cache(self, client, market_data_service: MarketDataService):
        settings = MarketDataCacheSettings(base_cache_dir=Path(tempfile.gettempdir()))
        market_data_cache = MarketDataCache(
            settings=settings, services=client
        )
        figi = uuid.uuid4().hex
        from_ = now() - timedelta(days=30)
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            )
        )
        market_data_service.get_candles.reset_mock()

        from_cache = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            )
        )

        market_data_service.get_candles.assert_not_called()
        assert len(from_net) == len(from_cache)
        for cached_candle, net_candle in zip(from_cache, from_net):
            assert cached_candle.__repr__() == net_candle.__repr__()
