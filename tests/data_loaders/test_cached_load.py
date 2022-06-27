import logging
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, List
from unittest.mock import call

import pytest

from tinkoff.invest import (
    CandleInterval,
    Client,
    GetCandlesResponse,
    HistoricCandle,
    Quotation,
)
from tinkoff.invest.caching.cache_settings import (
    FileMetaData,
    MarketDataCacheSettings,
    meta_file_context,
)
from tinkoff.invest.caching.instrument_market_data_storage import (
    InstrumentMarketDataStorage,
)
from tinkoff.invest.services import MarketDataCache, MarketDataService
from tinkoff.invest.utils import candle_interval_to_timedelta, now, floor_datetime, \
    ceil_datetime

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_historical_candle(time: datetime, is_complete: bool = True):
    quotation = Quotation(units=100, nano=0)
    return HistoricCandle(
        open=quotation,
        high=quotation,
        low=quotation,
        close=quotation,
        volume=100,
        time=time,
        is_complete=is_complete,
    )


def get_candles_response(start: datetime, end: datetime, interval: CandleInterval):
    delta = candle_interval_to_timedelta(interval)
    start_ceil = ceil_datetime(start.replace(second=0, microsecond=0), delta)
    current_time = start_ceil
    candles = []
    while current_time <= end:
        candles.append(get_historical_candle(current_time))
        current_time += delta
        current_time.replace(second=0, microsecond=0)

    if floor_datetime(end, delta) < end < ceil_datetime(end, delta):
        candles.append(get_historical_candle(end, is_complete=False))

    return GetCandlesResponse(candles=candles)


@pytest.fixture()
def market_data_service(mocker) -> MarketDataService:
    service = mocker.Mock(spec=MarketDataService)

    def _get_candles(
        figi: str,
        from_: datetime,
        to: datetime,
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
def market_data_cache(settings: MarketDataCacheSettings, client) -> MarketDataCache:
    return MarketDataCache(settings=settings, services=client)


@pytest.fixture()
def log(caplog):  # noqa: PT004
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
        interval = CandleInterval.CANDLE_INTERVAL_HOUR
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=from_, end=to, interval=interval)
        market_data_service.get_candles.reset_mock()

        from_cache = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=interval,
            )
        )
        market_data_service.get_candles.assert_not_called()
        self.assert_in_range(from_cache, start=from_, end=to, interval=interval)
        assert len(from_net) == len(from_cache)
        for cached_candle, net_candle in zip(from_cache, from_net):
            assert cached_candle.__repr__() == net_candle.__repr__()

    def test_loads_from_cache_and_left_from_net(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache
    ):
        figi = uuid.uuid4().hex
        to = now().replace(second=0, microsecond=0)
        from_ = to - timedelta(days=30)
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=from_, end=to, interval=interval)
        from_cache = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=interval,
            )
        )
        self.assert_in_range(from_cache, start=from_, end=to, interval=interval)
        market_data_service.get_candles.reset_mock()
        from_early_uncached = from_ - timedelta(days=7)

        cache_and_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_early_uncached,
                to=to,
                interval=interval,
            )
        )

        assert len(market_data_service.get_candles.mock_calls) > 0
        self.assert_in_range(cache_and_net, start=from_early_uncached, end=to, interval=interval)

    def assert_in_range(self, result_candles, start, end, interval):
        delta = candle_interval_to_timedelta(interval)
        assert result_candles[0].time == ceil_datetime(start, delta), "start time assertion error"
        assert result_candles[-1].time == floor_datetime(end, delta), "end time assertion error"
        for candle in result_candles:
            assert start <= candle.time <= end

    def test_loads_from_cache_and_right_from_net(
        self, market_data_service: MarketDataService, market_data_cache: MarketDataCache
    ):
        figi = uuid.uuid4().hex
        to = now().replace(second=0, microsecond=0)
        from_ = to - timedelta(days=30)
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        from_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=interval,
            )
        )
        self.assert_in_range(from_net, start=from_, end=to, interval=interval)
        market_data_service.get_candles.reset_mock()
        to_later_uncached = to + timedelta(days=7)

        cache_and_net = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=from_,
                to=to_later_uncached,
                interval=interval,
            )
        )

        assert len(market_data_service.get_candles.mock_calls) > 0
        self.assert_in_range(cache_and_net, start=from_, end=to_later_uncached, interval=interval)

    def assert_has_cached_ranges(self, cache_storage, ranges):
        meta_file = cache_storage._get_metafile(cache_storage._meta_path)
        with meta_file_context(meta_file) as meta:
            meta: FileMetaData = meta
            assert len(meta.cached_range_in_file) == len(ranges)
            assert set(meta.cached_range_in_file.keys()) == set(ranges)

    def assert_file_count(self, cache_storage, count):
        cached_ls = list(cache_storage._meta_path.parent.glob("*"))
        assert len(cached_ls) == count

    def test_loads_cache_miss(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        # [A request B]
        # [A cached  B]  [C request D]
        A, B, C, D = self._get_date_point_by_index(0, 3, 6, 9)
        self.get_by_range_and_assert_has_cache(
            range=(A, B),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(C, D),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, B), (C, D)])
        self.assert_file_count(cache_storage, 3)

    def test_loads_cache_merge_middle(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        # [A request B]
        # [A cached  B]  [C request D]
        # [A cached  B]  [C cached  D]
        #        [E request F]
        # [A         cached         D]
        A, E, B, C, F, D = self._get_date_point_by_index(0, 2, 3, 6, 7, 9)
        self.get_by_range_and_assert_has_cache(
            range=(A, B),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(C, D),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        self.get_by_range_and_assert_has_cache(
            range=(E, F),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, D)])
        self.assert_file_count(cache_storage, 2)

    def _get_date_point_by_index(self, *idx, interval=CandleInterval.CANDLE_INTERVAL_DAY):
        delta = candle_interval_to_timedelta(interval)
        x0 = ceil_datetime(now(), delta).replace(second=0, microsecond=0)

        result = []
        for id_ in idx:
            result.append(x0 + id_ * delta)
        return result

    def test_loads_cache_merge_out(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
        log,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        #   [A request B]
        #   [A cached  B]  [C request D]
        #   [A cached  B]  [C cached  D]
        # [E           request           F]
        # [E           cached            F]
        E, A, B, C, D, F = self._get_date_point_by_index(0, 1, 3, 4, 6, 7)
        self.get_by_range_and_assert_has_cache(
            range=(A, B),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(C, D),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(E, F),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(E, F)])
        self.assert_file_count(cache_storage, 2)

    def get_by_range_and_assert_has_cache(
        self,
        range: Tuple[datetime, datetime],
        has_from_net: bool,
        figi: str,
        interval: CandleInterval,
        market_data_cache: MarketDataCache,
        market_data_service: MarketDataService,
    ):
        start, end = range
        result = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=start,
                to=end,
                interval=interval,
            )
        )
        self.assert_in_range(result, start=start, end=end, interval=interval)
        if has_from_net:
            assert (
                len(market_data_service.get_candles.mock_calls) > 0
            ), "Net was not used"
        else:
            assert len(market_data_service.get_candles.mock_calls) == 0, "Net was used"
        market_data_service.get_candles.reset_mock()

    def get_by_range_and_assert_ranges(
        self,
        request_range: Tuple[datetime, datetime],
        from_cache_ranges: List[Tuple[datetime, datetime]],
        from_net_ranges: List[Tuple[datetime, datetime]],
        figi: str,
        interval: CandleInterval,
        market_data_cache: MarketDataCache,
        market_data_service: MarketDataService,
    ):
        start, end = request_range
        result = list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=start,
                to=end,
                interval=interval,
            )
        )
        net_calls = market_data_service.get_candles.mock_calls
        assert len(net_calls) == len(from_net_ranges)
        for actual_net_call, expected_net_range in zip(net_calls, from_net_ranges):
            kwargs = actual_net_call.kwargs
            actual_net_range = kwargs['from_'], kwargs['to']
            assert actual_net_range == expected_net_range

        market_data_service.get_candles.reset_mock()

    def test_loads_cache_merge_out_left(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
        log,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        #   [A request B]
        #   [A cached  B]  [C request D]
        #   [A cached  B]  [C cached  D]
        # [E           request    F]
        # [E           cached         D]
        E, A, B, C, F, D = self._get_date_point_by_index(0, 1, 3, 4, 6, 7)
        self.get_by_range_and_assert_has_cache(
            range=(A, B),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(C, D),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(E, F),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(E, D)])
        self.assert_file_count(cache_storage, 2)

    def test_loads_cache_merge_out_right(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
        log,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        #   [A request B]
        #   [A cached  B]  [C request D]
        #   [A cached  B]  [C cached  D]
        #       [E    request            F]
        #   [A         cached            F]
        A, E, B, C, D, F = self._get_date_point_by_index(0, 1, 3, 4, 6, 7)
        self.get_by_range_and_assert_has_cache(
            range=(A, B),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(C, D),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(E, F),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, F)])
        self.assert_file_count(cache_storage, 2)

    def test_loads_cache_merge_in_right(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
        log,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        #   [A request B]
        #   [A cached  B]  [C request D]
        #   [A cached  B]  [C cached  D]
        #                     [E request F]
        #   [A cached  B]  [C   cached   F]
        A, B, C, E, D, F = self._get_date_point_by_index(0, 1, 3, 4, 6, 7)
        self.get_by_range_and_assert_has_cache(
            range=(A, B),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(C, D),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_has_cache(
            range=(E, F),
            has_from_net=True,
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, B), (C, F)])
        self.assert_file_count(cache_storage, 3)

    def test_creates_files_with_correct_extensions(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
        log,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_HOUR

        list(
            market_data_cache.get_all_candles(
                figi=figi,
                from_=now() - timedelta(days=30),
                interval=interval,
            )
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        cached_ls = list(cache_storage._meta_path.parent.glob("*"))
        assert len(cached_ls) == 2
        assert any(
            str(file).endswith(f".{settings.format_extension}") for file in cached_ls
        )
        assert any(
            str(file).endswith(f".{settings.meta_extension}") for file in cached_ls
        )

    def test_do_not_cache_if_is_not_complete_candle(
        self,
        market_data_service: MarketDataService,
        market_data_cache: MarketDataCache,
        settings: MarketDataCacheSettings,
        log,
    ):
        figi = uuid.uuid4().hex
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        # +: is_complete=True
        # -: is_complete=False
        #   1   2   3   4   5   6   7
        #   +---+---+---+---+---+---+
        #   [A    request    D]
        #   [A    cached   C]
        #     [B    request       F]
        #   [A    cached       E]
        A, B, C, D, E, F = self._get_date_point_by_index(1, 1.5, 5, 5.5, 6, 6.6, interval=interval)
        self.get_by_range_and_assert_ranges(
            request_range=(A, D),
            from_cache_ranges=[],
            from_net_ranges=[(A, D)],
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )
        self.get_by_range_and_assert_ranges(
            request_range=(B, F),
            from_cache_ranges=[(B, C)],
            from_net_ranges=[(C, F)],
            figi=figi,
            interval=interval,
            market_data_cache=market_data_cache,
            market_data_service=market_data_service,
        )

        cache_storage = InstrumentMarketDataStorage(
            figi=figi, interval=interval, settings=settings
        )
        self.assert_has_cached_ranges(cache_storage, [(A, E)])
        self.assert_file_count(cache_storage, 2)
