from datetime import datetime, timedelta
from typing import Generator, Optional, Tuple

from .schemas import CandleInterval, HistoricCandle
from .services import MarketDataService

__all__ = ("get_all_candles",)

DAYS_IN_YEAR = 365


MAX_INTERVALS = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(weeks=1),
    CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=DAYS_IN_YEAR),
}


def _get_intervals(
    interval: CandleInterval, from_: datetime, to: datetime
) -> Generator[Tuple[datetime, datetime], None, None]:
    max_interval = MAX_INTERVALS[interval]
    local_from = from_
    while local_from < to:
        yield local_from, min(local_from + max_interval, to)
        local_from += max_interval


def get_all_candles(
    service: MarketDataService,
    *,
    from_: datetime,
    to: Optional[datetime] = None,
    interval: CandleInterval = CandleInterval(0),
    figi: str = "",
) -> Generator[HistoricCandle, None, None]:
    to = to or datetime.utcnow()

    for local_from_, local_to in _get_intervals(interval, from_, to):
        candles_response = service.get_candles(
            figi=figi,
            interval=interval,
            from_=local_from_,
            to=local_to,
        )
        yield from candles_response.candles
