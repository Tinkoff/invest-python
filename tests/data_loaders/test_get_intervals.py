# pylint:disable=protected-access
from datetime import datetime

import pytest

from tinkoff.invest.data_loaders import _get_intervals
from tinkoff.invest.schemas import CandleInterval


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
        _get_intervals(
            candle_interval,
            *interval,
        )
    )

    assert result == intervals
