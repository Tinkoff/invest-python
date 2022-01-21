from datetime import datetime, timedelta
from typing import Generator, Optional

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

__all__ = ("MarketDataServiceHelper",)

DAYS_IN_YEAR = 365


class MarketDataServiceHelper:
    def __init__(self, service: MarketDataService) -> None:
        self._service = service

    def get_candles(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
    ) -> Generator[HistoricCandle, None, None]:
        request = GetCandlesRequest()
        request.figi = figi
        request.interval = interval

        if not from_ or not to:
            if from_ is not None:
                request.from_ = from_
            if to is not None:
                request.to = to
            candles_response = self._request_candles(request)
            yield from candles_response.candles
            return

        for local_from_, local_to in self._separate_date_for_intervals(
            from_, to, interval
        ):
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

    @staticmethod
    def _separate_date_for_intervals(
        from_: datetime,
        to: datetime,
        candle_interval: CandleInterval,
    ) -> Generator[tuple[datetime, datetime], None, None]:
        max_interval_for_candle_intervals = {
            CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(days=1),
            CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(days=1),
            CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(days=1),
            CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(weeks=1),
            CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=DAYS_IN_YEAR),
        }
        max_interval_for_candle_interval = max_interval_for_candle_intervals[
            candle_interval
        ]
        while from_ + max_interval_for_candle_interval < to:
            yield to - max_interval_for_candle_interval, to
            to -= max_interval_for_candle_interval
        yield from_, to
