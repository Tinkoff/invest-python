from datetime import datetime
from typing import Tuple

import pytest

from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import round_datetime_range


@pytest.mark.parametrize(
    ("interval", "date_range", "expected_range"),
    [
        (
            CandleInterval.CANDLE_INTERVAL_1_MIN,
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=1, second=1, microsecond=1
                ),
                datetime(
                    year=2023, month=1, day=2, hour=1, minute=1, second=1, microsecond=1
                ),
            ),
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=1, second=0, microsecond=0
                ),
                datetime(
                    year=2023, month=1, day=2, hour=1, minute=2, second=0, microsecond=0
                ),
            ),
        ),
        (
            CandleInterval.CANDLE_INTERVAL_HOUR,
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=1, second=1, microsecond=1
                ),
                datetime(
                    year=2023, month=1, day=2, hour=1, minute=1, second=1, microsecond=1
                ),
            ),
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=0, second=0, microsecond=0
                ),
                datetime(
                    year=2023, month=1, day=2, hour=2, minute=0, second=0, microsecond=0
                ),
            ),
        ),
        (
            CandleInterval.CANDLE_INTERVAL_DAY,
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=1, second=1, microsecond=1
                ),
                datetime(
                    year=2023, month=1, day=2, hour=1, minute=1, second=1, microsecond=1
                ),
            ),
            (
                datetime(
                    year=2023, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                ),
                datetime(
                    year=2023, month=1, day=3, hour=0, minute=0, second=0, microsecond=0
                ),
            ),
        ),
        (
            CandleInterval.CANDLE_INTERVAL_WEEK,
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=1, second=1, microsecond=1
                ),
                datetime(
                    year=2023, month=1, day=2, hour=1, minute=1, second=1, microsecond=1
                ),
            ),
            (
                datetime(
                    year=2023, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                ),
                datetime(
                    year=2023, month=1, day=9, hour=0, minute=0, second=0, microsecond=0
                ),
            ),
        ),
        (
            CandleInterval.CANDLE_INTERVAL_MONTH,
            (
                datetime(
                    year=2023, month=1, day=1, hour=1, minute=1, second=1, microsecond=1
                ),
                datetime(
                    year=2023, month=1, day=2, hour=1, minute=1, second=1, microsecond=1
                ),
            ),
            (
                datetime(
                    year=2023, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                ),
                datetime(
                    year=2023, month=2, day=1, hour=0, minute=0, second=0, microsecond=0
                ),
            ),
        ),
    ],
)
def test_round_datetime_range(
    interval: CandleInterval,
    date_range: Tuple[datetime, datetime],
    expected_range: Tuple[datetime, datetime],
):
    actual_range = round_datetime_range(
        date_range=date_range,
        interval=interval,
    )

    assert actual_range == expected_range
