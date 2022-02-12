import abc

from tinkoff.invest.strategies.base.signal import Signal


class ISignalExecutor(abc.ABC):
    @abc.abstractmethod
    def execute(self, signal: Signal) -> None:
        pass
