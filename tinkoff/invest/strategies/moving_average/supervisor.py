from itertools import chain
from typing import Iterable, List, Type, Dict, cast

from tinkoff.invest.strategies.base.errors import EventsWereNotSupervised
from tinkoff.invest.strategies.base.event import StrategyEvent
from tinkoff.invest.strategies.base.strategy_supervisor import StrategySupervisor, \
    TEvent


class MovingAverageStrategySupervisor(StrategySupervisor):
    def __init__(self):
        self._events: Dict[Type[StrategyEvent], List[StrategyEvent]] = {}

    def notify(self, event: StrategyEvent) -> None:
        if type(event) not in self._events:
            self._events[type(event)] = []
        self._events[type(event)].append(event)

    def get_events(self) -> Iterable[StrategyEvent]:
        return cast(Iterable[StrategyEvent], chain(*self._events.values()))

    def get_events_of_type(self, cls: Type[TEvent]) -> Iterable[TEvent]:
        if cls in self._events:
            return self._events[cls]
        raise EventsWereNotSupervised()
