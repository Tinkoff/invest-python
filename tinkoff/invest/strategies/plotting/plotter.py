import abc
import logging
from typing import Iterable, List, NewType, Protocol

import mplfinance as mpf

from tinkoff.invest.strategies.base.event import StrategyEvent

PlotKwargs = NewType("PlotKwargs", dict)

logger = logging.getLogger(__name__)


class IPlotter(Protocol):
    def plot(self, plot_events: Iterable[StrategyEvent]) -> None:
        pass


class StrategyPlotter(abc.ABC, IPlotter):
    @abc.abstractmethod
    def get_candle_plot_kwargs(
        self, strategy_events: List[StrategyEvent]
    ) -> PlotKwargs:
        pass

    @abc.abstractmethod
    def get_signal_plot_kwargs(
        self, strategy_events: List[StrategyEvent]
    ) -> List[PlotKwargs]:
        pass

    def plot(self, strategy_events: Iterable[StrategyEvent]) -> None:
        strategy_events = list(strategy_events)
        candle_plot = self.get_candle_plot_kwargs(strategy_events=strategy_events)
        if signal_plots := self.get_signal_plot_kwargs(strategy_events=strategy_events):
            add_plots = [
                mpf.make_addplot(**signal_plot) for signal_plot in signal_plots
            ]
            candle_plot |= dict(addplot=add_plots)
        mpf.plot(**candle_plot)

        mpf.show()
