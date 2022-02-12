import abc
from typing import Iterable

from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal import Signal


class InvestStrategy(abc.ABC):
    @abc.abstractmethod
    def fit(self, candles: Iterable[CandleEvent]) -> None:
        pass

    @abc.abstractmethod
    def observe(self, candle: CandleEvent) -> None:
        pass

    @abc.abstractmethod
    def predict(self) -> Iterable[Signal]:
        pass
