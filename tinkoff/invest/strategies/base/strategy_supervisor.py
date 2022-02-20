import abc
from typing import Iterable, Protocol, Type

from tinkoff.invest.strategies.base.event import StrategyEvent


class IStrategySupervisor(Protocol):
    def notify(self, event: StrategyEvent) -> None:
        pass

    def get_events(self) -> Iterable[StrategyEvent]:
        pass

    def get_events_of_type(self, cls: Type[StrategyEvent]) -> Iterable[StrategyEvent]:
        pass


class StrategySupervisor(abc.ABC, IStrategySupervisor):
    @abc.abstractmethod
    def notify(self, event: StrategyEvent) -> None:
        pass

    @abc.abstractmethod
    def get_events(self) -> Iterable[StrategyEvent]:
        pass

    @abc.abstractmethod
    def get_events_of_type(self, cls: Type[StrategyEvent]) -> Iterable[StrategyEvent]:
        pass
