import ast
import dataclasses
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Callable, Generator, Iterable, List, Protocol, Tuple

import dateutil.parser

from .schemas import CandleInterval, HistoricCandle, Quotation, SubscriptionInterval

__all__ = (
    "get_intervals",
    "quotation_to_decimal",
    "decimal_to_quotation",
    "candle_interval_to_subscription_interval",
    "now",
    "candle_interval_to_timedelta",
    "ceil_datetime",
    "floor_datetime",
    "dataclass_from_dict",
    "round_datetime_range",
)

DAYS_IN_YEAR = 365


MAX_INTERVALS = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_2_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_3_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_10_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_30_MIN: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(weeks=1),
    CandleInterval.CANDLE_INTERVAL_2_HOUR: timedelta(weeks=1),
    CandleInterval.CANDLE_INTERVAL_4_HOUR: timedelta(weeks=1),
    CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=DAYS_IN_YEAR),
    CandleInterval.CANDLE_INTERVAL_WEEK: timedelta(days=DAYS_IN_YEAR),
    CandleInterval.CANDLE_INTERVAL_MONTH: timedelta(days=DAYS_IN_YEAR * 3),
}


def get_intervals(
    interval: CandleInterval, from_: datetime, to: datetime
) -> Generator[Tuple[datetime, datetime], None, None]:
    max_interval = MAX_INTERVALS[interval]
    local_from = from_
    interval_timedelta = candle_interval_to_timedelta(interval)
    while local_from + interval_timedelta <= to:
        yield local_from, min(local_from + max_interval, to)
        local_from += max_interval


def quotation_to_decimal(quotation: Quotation) -> Decimal:
    return money_to_decimal(quotation)


def decimal_to_quotation(decimal: Decimal) -> Quotation:
    fractional = decimal % 1
    return Quotation(units=int(decimal // 1), nano=int(fractional * Decimal("10e8")))


class MoneyProtocol(Protocol):
    units: int
    nano: int


def money_to_decimal(money: MoneyProtocol) -> Decimal:
    fractional = money.nano / Decimal("10e8")
    return Decimal(money.units) + fractional


# fmt: off
_CANDLE_INTERVAL_TO_SUBSCRIPTION_INTERVAL_MAPPING = {
    CandleInterval.CANDLE_INTERVAL_1_MIN:
        SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
    CandleInterval.CANDLE_INTERVAL_5_MIN:
        SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIVE_MINUTES,
    CandleInterval.CANDLE_INTERVAL_UNSPECIFIED:
        SubscriptionInterval.SUBSCRIPTION_INTERVAL_UNSPECIFIED,
}
# fmt: on


def candle_interval_to_subscription_interval(
    candle_interval: CandleInterval,
) -> SubscriptionInterval:
    return _CANDLE_INTERVAL_TO_SUBSCRIPTION_INTERVAL_MAPPING.get(
        candle_interval, SubscriptionInterval.SUBSCRIPTION_INTERVAL_UNSPECIFIED
    )


def now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


_CANDLE_INTERVAL_TO_TIMEDELTA_MAPPING = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: timedelta(minutes=1),
    CandleInterval.CANDLE_INTERVAL_2_MIN: timedelta(minutes=2),
    CandleInterval.CANDLE_INTERVAL_3_MIN: timedelta(minutes=3),
    CandleInterval.CANDLE_INTERVAL_5_MIN: timedelta(minutes=5),
    CandleInterval.CANDLE_INTERVAL_10_MIN: timedelta(minutes=10),
    CandleInterval.CANDLE_INTERVAL_15_MIN: timedelta(minutes=15),
    CandleInterval.CANDLE_INTERVAL_30_MIN: timedelta(minutes=30),
    CandleInterval.CANDLE_INTERVAL_HOUR: timedelta(hours=1),
    CandleInterval.CANDLE_INTERVAL_2_HOUR: timedelta(hours=2),
    CandleInterval.CANDLE_INTERVAL_4_HOUR: timedelta(hours=4),
    CandleInterval.CANDLE_INTERVAL_DAY: timedelta(days=1),
    CandleInterval.CANDLE_INTERVAL_WEEK: timedelta(weeks=1),
    CandleInterval.CANDLE_INTERVAL_MONTH: timedelta(days=30),
    CandleInterval.CANDLE_INTERVAL_UNSPECIFIED: timedelta(minutes=1),
}


def candle_interval_to_timedelta(candle_interval: CandleInterval) -> timedelta:
    if delta := _CANDLE_INTERVAL_TO_TIMEDELTA_MAPPING.get(candle_interval):
        return delta
    raise ValueError(f"Cannot convert {candle_interval} to timedelta")


_DATETIME_MIN = datetime.min.replace(tzinfo=timezone.utc)


def ceil_datetime(datetime_: datetime, delta: timedelta):
    return datetime_ + (_DATETIME_MIN - datetime_) % delta


def floor_datetime(datetime_: datetime, delta: timedelta):
    return datetime_ - (datetime_ - _DATETIME_MIN) % delta


def dataclass_from_dict(klass, d):
    if issubclass(int, klass):
        return int(d)
    if issubclass(bool, klass):
        return bool(d)
    if issubclass(klass, datetime):
        return dateutil.parser.parse(d).replace(tzinfo=timezone.utc)
    if issubclass(klass, Quotation):
        d = ast.literal_eval(d)
    fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
    return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})


_datetime_range_replace_floor_by_interval = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_2_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_3_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_5_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_10_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_15_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_30_MIN: lambda r: r.replace(second=0, microsecond=0),
    CandleInterval.CANDLE_INTERVAL_HOUR: lambda r: r.replace(
        minute=0, second=0, microsecond=0
    ),
    CandleInterval.CANDLE_INTERVAL_2_HOUR: lambda r: r.replace(
        minute=0, second=0, microsecond=0
    ),
    CandleInterval.CANDLE_INTERVAL_4_HOUR: lambda r: r.replace(
        minute=0, second=0, microsecond=0
    ),
    CandleInterval.CANDLE_INTERVAL_DAY: lambda r: r.replace(
        hour=0, minute=0, second=0, microsecond=0
    ),
    CandleInterval.CANDLE_INTERVAL_WEEK: lambda r: r.replace(
        hour=0, minute=0, second=0, microsecond=0
    ),
    CandleInterval.CANDLE_INTERVAL_MONTH: lambda r: r.replace(
        hour=0, minute=0, second=0, microsecond=0
    ),
}


def round_datetime_range(
    date_range: Tuple[datetime, datetime],
    interval: CandleInterval,
) -> Tuple[datetime, datetime]:
    """Округляет диапазон до ближайшего целого диапазона, в зависимости от interval."""
    floor = _datetime_range_replace_floor_by_interval[interval]
    start, end = date_range
    start = floor(start)
    interval_delta = candle_interval_to_timedelta(interval)
    end = floor(end + interval_delta)
    return start, end


def filter_distinct_candles(candles: List[HistoricCandle]) -> List[HistoricCandle]:
    filtered = []
    for candle1, candle2 in zip(candles, candles[1:]):
        if candle2.time - candle1.time > timedelta():
            filtered.append(candle1)
    filtered.extend(candles[-1:])
    return filtered


def with_filtering_distinct_candles(f: Callable[[Any], Iterable[HistoricCandle]]):
    def _(*args: Any, **kwargs: Any) -> Iterable[HistoricCandle]:
        yield from filter_distinct_candles(list(f(*args, **kwargs)))

    return _
