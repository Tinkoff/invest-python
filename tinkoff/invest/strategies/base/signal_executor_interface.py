from typing import Protocol

from tinkoff.invest.strategies.base.signal import Signal


class ISignalExecutor(Protocol):
    def execute(self, signal: Signal) -> None:
        pass
