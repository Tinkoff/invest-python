from datetime import timedelta

import pytest

from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import (
    candle_interval_to_timedelta,
    ceil_datetime,
    floor_datetime,
    now,
)


@pytest.fixture(params=[i.value for i in CandleInterval])
def interval(request) -> timedelta:
    return candle_interval_to_timedelta(request.param)


def test_floor_ceil(interval: timedelta):
    now_ = now()

    a, b = floor_datetime(now_, interval), ceil_datetime(now_, interval)

    assert a < b
    assert b - a == interval
