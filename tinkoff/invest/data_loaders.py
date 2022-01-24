from datetime import datetime, timedelta
from typing import Generator, Optional, Tuple

from tinkoff.invest import (
    CandleInterval,
    GetCandlesRequest,
    GetCandlesResponse,
    HistoricCandle,
    _grpc_helpers,
)
from tinkoff.invest.grpc import marketdata_pb2
from tinkoff.invest.logging import get_tracking_id_from_call, log_request
from tinkoff.invest.services import MarketDataService

__all__ = ("MarketDataLoader",)

DAYS_IN_YEAR = 365


class MarketDataLoaderException(Exception):
    pass


class MarketDataLoader:
    def __init__(
        self,
        *,
        service: MarketDataService,
        from_: datetime,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
        figi: str = "",
    ) -> None:
        self._service: MarketDataService = service
        self._figi: str = figi
        self._interval: CandleInterval = interval
        self._from: datetime = from_
        self._to: datetime = to or datetime.utcnow()

    def __iter__(self):
        yield from self.candles

    @property
    def candles(self) -> Generator[HistoricCandle, None, None]:
        request = GetCandlesRequest()
        request.figi = self._figi
        request.interval = self._interval

        for local_from_, local_to in self.separated_date_for_intervals:
            request.from_ = local_from_
            request.to = local_to
            candles_response = self._request_candles(request)
            yield from candles_response.candles

    def _request_candles(self, request: GetCandlesRequest) -> GetCandlesResponse:
        response, call = self._service.stub.GetCandles.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetCandlesRequest()
            ),
            metadata=self._service.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetCandles")
        return _grpc_helpers.protobuf_to_dataclass(response, GetCandlesResponse)

    @property
    def separated_date_for_intervals(
        self,
    ) -> Generator[Tuple[datetime, datetime], None, None]:
        max_interval_for_candle_intervals = {
            CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(days=1),
            CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(days=1),
            CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(days=1),
            CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(weeks=1),
            CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=DAYS_IN_YEAR),
        }
        max_interval_for_candle_interval = max_interval_for_candle_intervals[
            self._interval
        ]
        local_to = self._to
        while self._from + max_interval_for_candle_interval < local_to:
            yield local_to - max_interval_for_candle_interval, local_to
            local_to -= max_interval_for_candle_interval
        yield self._from, local_to
