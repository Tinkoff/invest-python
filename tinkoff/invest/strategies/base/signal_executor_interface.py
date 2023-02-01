from typing import Protocol

from .signal import Signal


class ISignalExecutor(Protocol):
    def execute(self, signal: Signal) -> None:
        pass
