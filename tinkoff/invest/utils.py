from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Generator, Tuple

from .schemas import CandleInterval, Quotation, SubscriptionInterval

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
    while local_from < to:
        yield local_from, min(local_from + max_interval, to)
        local_from += max_interval


def quotation_to_decimal(quotation: Quotation) -> Decimal:
    fractional = quotation.nano / Decimal("10e8")
    return Decimal(quotation.units) + fractional


def decimal_to_quotation(decimal: Decimal) -> Quotation:
    fractional = decimal % 1
    return Quotation(units=int(decimal // 1), nano=int(fractional * Decimal("10e8")))


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
