import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Type, cast

import mplfinance as mpf
import numpy as np
import pandas as pd

from tinkoff.invest.strategies.base.event import DataEvent, SignalEvent, StrategyEvent
from tinkoff.invest.strategies.base.signal import (
    CloseLongMarketOrder,
    CloseShortMarketOrder,
    OpenLongMarketOrder,
    OpenShortMarketOrder,
    OrderSignal,
    Signal,
    SignalDirection,
)
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.plotting.plotter import PlotKwargs, StrategyPlotter

logger = logging.getLogger(__name__)


class MovingAverageStrategyPlotter(StrategyPlotter):
    def __init__(self, settings: MovingAverageStrategySettings):
        self._was_not_executed_color = "grey"
        self._settings = settings
        self._signal_type_to_style_map: Dict[Type[Signal], Dict[str, Any]] = {
            OpenLongMarketOrder: dict(
                type="scatter", markersize=50, marker="^", color="green"
            ),
            CloseLongMarketOrder: dict(
                type="scatter", markersize=50, marker="^", color="black"
            ),
            OpenShortMarketOrder: dict(
                type="scatter", markersize=50, marker="v", color="red"
            ),
            CloseShortMarketOrder: dict(
                type="scatter", markersize=50, marker="v", color="black"
            ),
        }

        self._signal_type_to_candle_point_map = {
            SignalDirection.LONG: lambda candle: candle.low,
            SignalDirection.SHORT: lambda candle: candle.high,
        }

    def _filter_data_events(
        self, strategy_events: List[StrategyEvent]
    ) -> List[DataEvent]:
        return cast(
            List[DataEvent],
            list(filter(lambda e: isinstance(e, DataEvent), strategy_events)),
        )

    def _filter_signal_events(
        self, strategy_events: List[StrategyEvent]
    ) -> List[SignalEvent]:
        return cast(
            List[SignalEvent],
            list(filter(lambda e: isinstance(e, SignalEvent), strategy_events)),
        )

    def _get_interval_count_between_dates(
        self, start: datetime, end: datetime, interval_delta: timedelta
    ) -> float:
        return (end - start) / interval_delta

    def get_candle_plot_kwargs(
        self, strategy_events: List[StrategyEvent]
    ) -> PlotKwargs:
        data_events = self._filter_data_events(strategy_events)
        quotes = {
            "open": [float(e.candle_event.candle.open) for e in data_events],
            "close": [float(e.candle_event.candle.close) for e in data_events],
            "high": [float(e.candle_event.candle.high) for e in data_events],
            "low": [float(e.candle_event.candle.low) for e in data_events],
            "volume": [float(e.candle_event.volume) for e in data_events],
            "time": [e.candle_event.time for e in data_events],
        }
        df = pd.DataFrame(quotes, index=quotes["time"])
        interval_count = self._get_interval_count_between_dates(
            start=df["time"].idxmin(),
            end=df["time"].idxmax(),
            interval_delta=self._settings.candle_interval_timedelta,
        )
        non_trading_coefficient = len(data_events) / interval_count
        mav = {
            "ma_short": int(
                self._settings.short_period
                / self._settings.candle_interval_timedelta
                * non_trading_coefficient
            ),
            "ma_long": int(
                self._settings.long_period
                / self._settings.candle_interval_timedelta
                * non_trading_coefficient
            ),
        }
        style = mpf.make_mpf_style(
            base_mpf_style="charles", mavcolors=["#1f77b4", "#ff7f0e", "#2ca02c"]
        )
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
                style=style,
                returnfig=True,
            ),
        )

    def _get_plot_for_signal_type(
        self,
        signal_type: Type[Signal],
        signal_event_types_to_event_index: Dict[Type[Signal], Dict[int, SignalEvent]],
        data_events: List[DataEvent],
        was_executed_flag: bool,
    ) -> Optional[PlotKwargs]:
        style = self._signal_type_to_style_map[signal_type]
        price = [np.NAN] * len(data_events)
        color = style["color"]
        has_signal = False
        for index, signal_event in signal_event_types_to_event_index[
            signal_type
        ].items():
            if was_executed_flag == signal_event.was_executed:
                has_signal = True
                candle = data_events[index].candle_event.candle
                signal = cast(OrderSignal, signal_event.signal)
                price[index] = self._signal_type_to_candle_point_map[signal.direction](
                    candle
                )
            if not signal_event.was_executed:
                color = self._was_not_executed_color
        if not has_signal:
            return None
        style |= dict(color=color)
        params = {
            "price": price,
            "time": [e.candle_event.time for e in data_events],
        }
        df = pd.DataFrame(params, index=params["time"])
        return cast(PlotKwargs, dict(data=df["price"], **style))

    def get_signal_plot_kwargs(
        self, strategy_events: List[StrategyEvent]
    ) -> List[PlotKwargs]:
        signal_events = self._filter_signal_events(strategy_events)
        data_events = self._filter_data_events(strategy_events)
        data_events.sort(key=lambda e: e.time)
        first_data_event, last_data_event = data_events[0], data_events[-1]
        data_events_timedelta = last_data_event.time - first_data_event.time

        signal_event_types_to_event_index: Dict[
            Type[Signal], Dict[int, SignalEvent]
        ] = {}
        for signal_event in signal_events:
            signal_type = type(signal_event.signal)
            event_index = int(
                ((signal_event.time - first_data_event.time) / data_events_timedelta)
                * len(data_events)
            )
            event_index = min(event_index, len(data_events) - 1)
            if signal_type not in signal_event_types_to_event_index:
                signal_event_types_to_event_index[signal_type] = {}
            signal_event_types_to_event_index[signal_type][event_index] = signal_event

        plots = []
        for was_executed_flag in [False, True]:
            for signal_type in signal_event_types_to_event_index:
                kwargs = self._get_plot_for_signal_type(
                    signal_type=signal_type,
                    signal_event_types_to_event_index=signal_event_types_to_event_index,
                    data_events=data_events,
                    was_executed_flag=was_executed_flag,
                )
                plots.append(kwargs)

        return cast(List[PlotKwargs], list(filter(lambda p: p is not None, plots)))
