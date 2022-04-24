import logging
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pytest

from tinkoff.invest import (
    CandleInterval,
    Client,
    GetCandlesResponse,
    HistoricCandle,
    Quotation,
)
from tinkoff.invest.caching.cache_settings import MarketDataCacheSettings, \
    meta_file_context, FileMetaData
from tinkoff.invest.caching.instrument_market_data_storage import \
    InstrumentMarketDataStorage
from tinkoff.invest.services import MarketDataCache, MarketDataService
from tinkoff.invest.utils import candle_interval_to_timedelta, now

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
    current_time = start.replace(second=0, microsecond=0)
    times = []
    while current_time <= end:
        times.append(current_time)
        current_time += delta
        current_time.replace(second=0, microsecond=0)

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


@pytest.fixture()
def settings() -> MarketDataCacheSettings:
    return MarketDataCacheSettings(base_cache_dir=Path(tempfile.gettempdir()))


@pytest.fixture()
def market_data_cache(settings: MarketDataCacheSettings, client: Client) -> MarketDataCache:
    return MarketDataCache(settings=settings, services=client)

@pytest.fixture()
def log(caplog):
    caplog.set_level(logging.DEBUG)


class TestCachedLoad:
    def test_loads_from_net(self, market_data_cache: MarketDataCache):
        result = list(
            market_data_cache.get_all_candles(
                figi=uuid.uuid4().hex,
                from_=now() - timedelta(days=30),
                interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            )
        )

        assert result

    def test_loads_from_net_then_from_cache(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache
    ):
        figi = uuid.uuid4().hex
        to = now().replace(second=0, microsecond=0)
        from_ = to - timedelta(days=30)
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            )
        )
        self.assert_in_range(from_net, start=from_, end=to)
        market_data_service.get_candles.reset_mock()

        from_cache = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            )
        )
        market_data_service.get_candles.assert_not_called()
        self.assert_in_range(from_cache, start=from_, end=to)
        assert len(from_net) == len(from_cache)
        for cached_candle, net_candle in zip(from_cache, from_net):
            assert cached_candle.__repr__() == net_candle.__repr__()

    def test_loads_from_cache_and_left_from_net(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache
    ):
        figi = uuid.uuid4().hex
        to = now().replace(second=0, microsecond=0)
        from_ = to - timedelta(days=30)
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            )
        )
        self.assert_in_range(from_net, start=from_, end=to)
        from_cache = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            )
        )
        self.assert_in_range(from_cache, start=from_, end=to)
        market_data_service.get_candles.reset_mock()
        from_early_uncached = from_ - timedelta(days=7)

        cache_and_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_early_uncached,
                to=to,
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            )
        )

        assert len(market_data_service.get_candles.mock_calls) > 0
        self.assert_in_range(cache_and_net, start=from_early_uncached, end=to)

    def assert_in_range(self, result_candles, start, end):
        assert result_candles[0].time == start, 'start time assertion error'
        assert result_candles[-1].time == end, 'end time assertion error'
        for candle in result_candles:
            assert start <= candle.time <= end

    def test_loads_from_cache_and_right_from_net(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache
    ):
        figi = uuid.uuid4().hex
        to = now().replace(second=0, microsecond=0)
        from_ = to - timedelta(days=30)
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            )
        )
        self.assert_in_range(from_net, start=from_, end=to)
        market_data_service.get_candles.reset_mock()
        to_later_uncached = to + timedelta(days=7)

        cache_and_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to_later_uncached,
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            )
        )

        assert len(market_data_service.get_candles.mock_calls) > 0
        self.assert_in_range(cache_and_net, start=from_, end=to_later_uncached)

    def assert_has_cached_ranges(self, cache_storage, ranges):
        meta_file = cache_storage._get_metafile(cache_storage._meta_path)
        with meta_file_context(meta_file) as meta:
            meta: FileMetaData = meta
            assert len(meta.cached_range_in_file) == len(ranges)
            for range in ranges:
                assert meta.cached_range_in_file.get(range) is not None

    def assert_file_count(self, cache_storage, count):
        cached_ls = list(cache_storage._meta_path.parent.glob('*'))
        assert len(cached_ls) == count

    def test_loads_cache_miss(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache, settings: MarketDataCacheSettings,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        # [A request B]
        # [A cached  B]  [C request D]
        D = now().replace(second=0, microsecond=0)
        C = D - timedelta(days=3)
        B = C - timedelta(days=3)
        A = B - timedelta(days=3)

        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=A,
                to=B,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=A, end=B)
        assert len(market_data_service.get_candles.mock_calls) > 0
        market_data_service.get_candles.reset_mock()
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=C,
                to=D,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=C, end=D)
        assert len(market_data_service.get_candles.mock_calls) > 0

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, B), (C, D)])
        self.assert_file_count(cache_storage, 3)

    def test_loads_cache_merge_middle(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache, settings: MarketDataCacheSettings,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        # [A request B]
        # [A cached  B]  [C request D]
        # [A cached  B]  [C cached  D]
        #        [E request F]
        # [A         cached         D]
        D = now().replace(second=0, microsecond=0)
        F = D - timedelta(days=3)
        C = F - timedelta(days=3)
        B = C - timedelta(days=3)
        E = B - timedelta(days=3)
        A = E - timedelta(days=3)
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=A,
                to=B,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=A, end=B)
        assert len(market_data_service.get_candles.mock_calls) > 0
        market_data_service.get_candles.reset_mock()
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=C,
                to=D,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=C, end=D)
        assert len(market_data_service.get_candles.mock_calls) > 0
        market_data_service.get_candles.reset_mock()

        from_merge = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=E,
                to=F,
                interval=interval,
            )
        )
        self.assert_in_range(from_merge, start=E, end=F)
        assert len(market_data_service.get_candles.mock_calls) > 0

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, D)])
        self.assert_file_count(cache_storage, 2)

    def _get_date_point_by_index(self, *idx, delta=timedelta(days=1)):
        x0 = now().replace(second=0, microsecond=0)

        result = []
        for id in idx:
            result.append(x0 + id*delta)
        return result

    def test_loads_cache_merge_out(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache, settings: MarketDataCacheSettings, log
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        #   [A request B]
        #   [A cached  B]  [C request D]
        #   [A cached  B]  [C cached  D]
        # [E           request           F]
        # [E           cached            F]
        E, A, B, C, D, F = self._get_date_point_by_index(0, 1, 3, 4, 6, 7)
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=A,
                to=B,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=A, end=B)
        assert len(market_data_service.get_candles.mock_calls) > 0
        market_data_service.get_candles.reset_mock()
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=C,
                to=D,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=C, end=D)
        assert len(market_data_service.get_candles.mock_calls) > 0
        market_data_service.get_candles.reset_mock()

        from_merge = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=E,
                to=F,
                interval=interval,
            )
        )
        self.assert_in_range(from_merge, start=E, end=F)
        assert len(market_data_service.get_candles.mock_calls) > 0
        market_data_service.get_candles.reset_mock()

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(E, F)])
        self.assert_file_count(cache_storage, 2)
