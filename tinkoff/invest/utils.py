from datetime import datetime, timedelta
from typing import Generator, Tuple

from .schemas import CandleInterval

__all__ = ("get_intervals",)

DAYS_IN_YEAR = 365


MAX_INTERVALS = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(weeks=1),
    CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=DAYS_IN_YEAR),
}


def get_intervals(
    interval: CandleInterval, from_: datetime, to: datetime
) -> Generator[Tuple[datetime, datetime], None, None]:
    max_interval = MAX_INTERVALS[interval]
    local_from = from_
    interval_timedelta = candle_interval_to_timedelta(interval)
    while local_from < to and to - local_from > interval_timedelta:
        yield local_from, min(local_from + max_interval, to)
        local_from += max_interval


_CANDLE_INTERVAL_TO_TIMEDELTA_MAPPING = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(minutes=1),
    CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(minutes=5),
    CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(minutes=15),
    CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(hours=1),
    CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_UNSPECIFIED: timedelta(minutes=1),
}


def candle_interval_to_timedelta(candle_interval: CandleInterval) -> timedelta:
    if delta := _CANDLE_INTERVAL_TO_TIMEDELTA_MAPPING.get(candle_interval):
        return delta
    raise ValueError(f"Cannot convert {candle_interval} to timedelta")
