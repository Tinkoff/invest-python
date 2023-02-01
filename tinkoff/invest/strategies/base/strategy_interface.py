from typing import Iterable, Protocol

from .models import CandleEvent
from .signal import Signal


class InvestStrategy(Protocol):
    def fit(self, candles: Iterable[CandleEvent]) -> None:
        pass

    def observe(self, candle: CandleEvent) -> None:
        pass

    def predict(self) -> Iterable[Signal]:
        pass
