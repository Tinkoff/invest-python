# pylint:disable=protected-access
from datetime import datetime

import pytest

from tinkoff.invest.schemas import CandleInterval
from tinkoff.invest.utils import get_intervals


@pytest.mark.parametrize(
    ("candle_interval", "interval", "intervals"),
    [
        (
            CandleInterval.CANDLE_INTERVAL_DAY,
            (datetime(2021, 1, 25, 0, 0), datetime(2022, 1, 25, 0, 1)),
            [
                (
                    datetime(2021, 1, 25, 0, 0),
                    datetime(2022, 1, 25, 0, 0),
                ),
                (
                    datetime(2022, 1, 25, 0, 0),
                    datetime(2022, 1, 25, 0, 1),
                ),
            ],
        ),
        (
            CandleInterval.CANDLE_INTERVAL_DAY,
            (datetime(2021, 1, 25, 0, 0), datetime(2022, 1, 25, 0, 0)),
            [
                (
                    datetime(2021, 1, 25, 0, 0),
                    datetime(2022, 1, 25, 0, 0),
                ),
            ],
        ),
        (
            CandleInterval.CANDLE_INTERVAL_DAY,
            (datetime(2021, 1, 25, 0, 0), datetime(2022, 1, 24, 0, 0)),
            [
                (
                    datetime(2021, 1, 25, 0, 0),
                    datetime(2022, 1, 24, 0, 0),
                ),
            ],
        ),
    ],
)
def test_get_intervals(candle_interval, interval, intervals):
    result = list(
        get_intervals(
            candle_interval,
            *interval,
        )
    )

    assert result == intervals
