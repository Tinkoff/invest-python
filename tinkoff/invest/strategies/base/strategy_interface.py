from typing import Iterable, Protocol

from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal import Signal


class InvestStrategy(Protocol):
    def fit(self, candles: Iterable[CandleEvent]) -> None:
        pass

    def observe(self, candle: CandleEvent) -> None:
        pass

    def predict(self) -> Iterable[Signal]:
        pass
