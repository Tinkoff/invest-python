# pylint:disable=redefined-builtin,too-many-lines
import abc
import logging
from datetime import datetime, timedelta
from typing import Dict, Generator, Iterable, Optional, Tuple

import grpc

from .caching.market_data_cache.cache_settings import MarketDataCacheSettings
from .caching.market_data_cache.instrument_date_range_market_data import (
    InstrumentDateRangeData,
)
from .caching.market_data_cache.instrument_market_data_storage import (
    InstrumentMarketDataStorage,
)
from .grpc import (
    instruments_pb2_grpc,
    marketdata_pb2_grpc,
    operations_pb2_grpc,
    orders_pb2,
    orders_pb2_grpc,
    sandbox_pb2_grpc,
    stoporders_pb2_grpc,
    users_pb2_grpc,
)
from .market_data_stream.market_data_stream_manager import MarketDataStreamManager
from .schemas import CandleInterval, GetCandlesResponse, HistoricCandle
from .typedefs import AccountId
from .utils import (
    candle_interval_to_timedelta,
    datetime_range_floor,
    floor_datetime,
    get_intervals,
    now,
    with_filtering_distinct_candles,
)

logger = logging.getLogger(__name__)


class ICandleGetter(abc.ABC):
    @abc.abstractmethod
    def get_all_candles(
        self,
        *,
        from_: datetime,
        to: Optional[datetime],
        interval: CandleInterval,
        figi: str,
    ) -> Generator[HistoricCandle, None, None]:
        pass


class MarketDataCache(ICandleGetter):
    def __init__(self, settings: MarketDataCacheSettings, services: "Services"):
        self._settings = settings
        self._settings.base_cache_dir.mkdir(parents=True, exist_ok=True)
        self._services = services
        self._figi_cache_storages: Dict[
            Tuple[str, CandleInterval], InstrumentMarketDataStorage
        ] = {}

    def _get_candles_from_net(
        self, figi: str, interval: CandleInterval, from_: datetime, to: datetime
    ) -> Iterable[HistoricCandle]:
        yield from self._services.get_all_candles(
            figi=figi,
            interval=interval,
            from_=from_,
            to=to,
        )

    def _with_saving_into_cache(
        self,
        storage: InstrumentMarketDataStorage,
        from_net: Iterable[HistoricCandle],
        net_range: Tuple[datetime, datetime],
        interval_delta: timedelta,
    ) -> Iterable[HistoricCandle]:
        candles = list(from_net)
        if candles:
            filtered_net_range = self._round_net_range(net_range, interval_delta)
            filtered_candles = list(self._filter_complete_candles(candles))
            storage.update(
                [
                    InstrumentDateRangeData(
                        date_range=filtered_net_range, historic_candles=filtered_candles
                    )
                ]
            )
            logger.debug("From net [\n%s\n%s\n]", str(net_range[0]), str(net_range[1]))
            logger.debug(
                "Filtered net [\n%s\n%s\n]",
                str(filtered_net_range[0]),
                str(filtered_net_range[1]),
            )
            logger.debug(
                "Filtered net real [\n%s\n%s\n]",
                str(min(list(map(lambda x: x.time, filtered_candles)))),  # noqa: C417
                str(max(list(map(lambda x: x.time, filtered_candles)))),  # noqa: C417
            )

        yield from candles

    def _filter_complete_candles(
        self, candles: Iterable[HistoricCandle]
    ) -> Iterable[HistoricCandle]:
        return filter(lambda candle: candle.is_complete, candles)

    @with_filtering_distinct_candles  # type: ignore
    def get_all_candles(
        self,
        *,
        from_: datetime,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
        figi: str = "",
    ) -> Generator[HistoricCandle, None, None]:
        interval_delta = candle_interval_to_timedelta(interval)
        to = to or now()
        from_, to = datetime_range_floor((from_, to))
        logger.debug("Request [\n%s\n%s\n]", str(from_), str(to))

        processed_time = from_
        figi_cache_storage = self._get_figi_cache_storage(figi=figi, interval=interval)
        for cached in figi_cache_storage.get(request_range=(from_, to)):
            cached_start, cached_end = cached.date_range
            cached_candles = list(cached.historic_candles)
            if cached_start > processed_time:
                yield from self._with_saving_into_cache(
                    storage=figi_cache_storage,
                    from_net=self._get_candles_from_net(
                        figi, interval, processed_time, cached_start
                    ),
                    net_range=(processed_time, cached_start),
                    interval_delta=interval_delta,
                )
            logger.debug(
                "Returning from cache [\n%s\n%s\n]", str(cached_start), str(cached_end)
            )

            yield from cached_candles
            processed_time = cached_end

        if processed_time + interval_delta <= to:
            yield from self._with_saving_into_cache(
                storage=figi_cache_storage,
                from_net=self._get_candles_from_net(figi, interval, processed_time, to),
                net_range=(processed_time, to),
                interval_delta=interval_delta,
            )

    def _get_figi_cache_storage(
        self, figi: str, interval: CandleInterval
    ) -> InstrumentMarketDataStorage:
        figi_tuple = (figi, interval)
        storage = self._figi_cache_storages.get(figi_tuple)
        if storage is None:
            storage = InstrumentMarketDataStorage(
                figi=figi, interval=interval, settings=self._settings
            )
            self._figi_cache_storages[figi_tuple] = storage
        return storage  # noqa:R504

    def _round_net_range(
        self, net_range: Tuple[datetime, datetime], interval_delta: timedelta
    ) -> Tuple[datetime, datetime]:
        start, end = net_range
        return start, floor_datetime(end, interval_delta)


class Services(ICandleGetter):
    def __init__(
        self,
        channel: grpc.Channel,
    ) -> None:
        self.instruments = instruments_pb2_grpc.InstrumentsServiceStub(channel)
        self.market_data = marketdata_pb2_grpc.MarketDataServiceStub(channel)
        self.market_data_stream = marketdata_pb2_grpc.MarketDataStreamServiceStub(
            channel
        )
        self.operations = operations_pb2_grpc.OperationsServiceStub(channel)
        self.operations_stream = operations_pb2_grpc.OperationsStreamServiceStub(
            channel
        )
        self.orders_stream = orders_pb2_grpc.OrdersStreamServiceStub(channel)
        self.orders = orders_pb2_grpc.OrdersServiceStub(channel)
        self.users = users_pb2_grpc.UsersServiceStub(channel)
        self.sandbox = sandbox_pb2_grpc.SandboxServiceStub(channel)
        self.stop_orders = stoporders_pb2_grpc.StopOrdersServiceStub(channel)

    def create_market_data_stream(self) -> MarketDataStreamManager:
        return MarketDataStreamManager(
            market_data_stream_service=self.market_data_stream
        )

    def cancel_all_orders(self, account_id: AccountId) -> None:
        orders_service: orders_pb2_grpc.OrdersServiceStub = self.orders
        stop_orders_service: stoporders_pb2_grpc.StopOrdersServiceStub = (
            self.stop_orders
        )

        orders_response = orders_service.get_orders(account_id=account_id)
        for order in orders_response.orders:
            orders_service.cancel_order(account_id=account_id, order_id=order.order_id)

        stop_orders_response = stop_orders_service.get_stop_orders(
            account_id=account_id
        )
        for stop_order in stop_orders_response.stop_orders:
            stop_orders_service.cancel_stop_order(
                account_id=account_id, stop_order_id=stop_order.stop_order_id
            )

    # pylint:disable=too-many-nested-blocks
    def get_all_candles(
        self,
        *,
        from_: datetime,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
        figi: str = "",
    ) -> Generator[HistoricCandle, None, None]:
        to = to or now()

        previous_candles = set()
        for current_from, current_to in get_intervals(interval, from_, to):
            candles_response: GetCandlesResponse = self.market_data.get_candles(
                figi=figi,
                interval=interval,
                from_=current_from,
                to=current_to,
            )

            for candle in candles_response.candles:
                if candle not in previous_candles:
                    yield candle
                    previous_candles.add(candle)

            previous_candles = set(candles_response.candles)
