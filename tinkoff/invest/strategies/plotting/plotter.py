import abc
import logging
from typing import Protocol, Iterable, NewType, cast, List

import mplfinance as mpf

from tinkoff.invest.strategies.base.event import StrategyEvent, DataEvent

PlotKwargs = NewType('PlotKwargs', dict)

logger = logging.getLogger(__name__)


class IPlotter(Protocol):
    def plot(self, plot_events: Iterable[StrategyEvent]) -> None:
        pass


class StrategyPlotter(abc.ABC, IPlotter):
    @abc.abstractmethod
    def get_candle_plot_kwargs(self, data_events: List[DataEvent]) -> PlotKwargs:
        pass

    def plot(self, plot_events: Iterable[StrategyEvent]) -> None:
        plot_events = list(plot_events)
        data_events = cast(List[DataEvent], list(filter(lambda e: isinstance(e, DataEvent), plot_events)))
        candle_plot = self.get_candle_plot_kwargs(data_events=data_events)

        mpf.plot(**candle_plot)

        mpf.show()
