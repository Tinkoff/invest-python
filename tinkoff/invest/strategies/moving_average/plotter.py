import logging
from typing import List, cast

import pandas as pd

from tinkoff.invest.strategies.moving_average.strategy_settings import \
    MovingAverageStrategySettings
from tinkoff.invest.strategies.base.event import DataEvent
from tinkoff.invest.strategies.plotting.plotter import StrategyPlotter, PlotKwargs

logger = logging.getLogger(__name__)


class MovingAverageStrategyPlotter(StrategyPlotter):
    def __init__(self, settings: MovingAverageStrategySettings):
        self._settings = settings

    def get_candle_plot_kwargs(self, data_events: List[DataEvent]) -> PlotKwargs:
        quotes = {
            "open": [float(e.candle_event.candle.open) for e in data_events],
            "close": [float(e.candle_event.candle.close) for e in data_events],
            "high": [float(e.candle_event.candle.high) for e in data_events],
            "low": [float(e.candle_event.candle.low) for e in data_events],
            "volume": [float(e.candle_event.volume) for e in data_events],
            "time": [e.candle_event.time for e in data_events],
        }
        df = pd.DataFrame(quotes, index=quotes["time"])
        mav = {
            "ma_short": int(
                self._settings.short_period / self._settings.candle_interval_timedelta
            ),
            "ma_long": int(
                self._settings.long_period / self._settings.candle_interval_timedelta
            ),
        }
        return cast(
            PlotKwargs,
            dict(
                data=df,
                type="candle",
                volume=True,
                figsize=(11, 8),
                panel_ratios=(2, 1),
                mav=tuple(mav.values()),
                title=self._settings.share_id,
                style="charles",
                returnfig=True,
            )
        )