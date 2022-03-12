import abc
import logging
from typing import Iterable, List, NewType, Protocol

import matplotlib.pyplot as plt
import mplfinance as mpf
from IPython.display import clear_output
from matplotlib.gridspec import GridSpec

from tinkoff.invest.strategies.base.event import StrategyEvent

PlotKwargs = NewType("PlotKwargs", dict)

logger = logging.getLogger(__name__)


class IPlotter(Protocol):
    def plot(self, strategy_events: Iterable[StrategyEvent]) -> None:
        pass


class StrategyPlotter(abc.ABC, IPlotter):
    def __init__(self):
        pass

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

    def get_plot_kwargs(self, strategy_events: Iterable[StrategyEvent]) -> PlotKwargs:
        strategy_events = list(strategy_events)
        candle_plot = self.get_candle_plot_kwargs(strategy_events=strategy_events)
        if signal_plots := self.get_signal_plot_kwargs(strategy_events=strategy_events):
            add_plots = []
            for signal_plot in signal_plots:
                signal_plot.update({"ax": self._ax1})
                ap = mpf.make_addplot(**signal_plot)
                add_plots.append(ap)

            candle_plot.update({"addplot": add_plots})
        return candle_plot

    def plot(self, strategy_events: Iterable[StrategyEvent]) -> None:
        self._fig = plt.figure(figsize=(20, 20))
        gs = GridSpec(2, 1, height_ratios=[3, 1])
        self._ax1 = plt.subplot(gs[0])
        self._ax2 = plt.subplot(gs[1])

        candle_plot_kwargs = self.get_plot_kwargs(strategy_events)
        candle_plot_kwargs.update({"ax": self._ax1, "volume": self._ax2})
        mpf.plot(**candle_plot_kwargs, warn_too_much_data=999999999)

        clear_output(wait=True)
        plt.show()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
