import abc
from abc import ABC
from functools import singledispatchmethod

from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.strategy.errors import UnknownSignal
from tinkoff.invest.strategy.signal import (
    CloseLongMarketOrder,
    CloseShortMarketOrder,
    OpenLongMarketOrder,
    OpenShortMarketOrder,
    Signal,
)
from tinkoff.invest.strategy.strategy import MovingAverageStrategyState


class ISignalExecutor(abc.ABC):
    @abc.abstractmethod
    def execute(self, signal: Signal) -> None:
        pass


class SignalExecutor(ISignalExecutor, ABC):
    def __init__(
        self,
        services: AsyncServices,
    ):
        self._services = services

    def _execute_open_long_market_order(self, signal: OpenLongMarketOrder) -> None:
        raise NotImplementedError()

    def _execute_close_long_market_order(self, signal: CloseLongMarketOrder) -> None:
        raise NotImplementedError()

    def _execute_open_short_market_order(self, signal: OpenShortMarketOrder) -> None:
        raise NotImplementedError()

    def _execute_close_short_market_order(self, signal: CloseShortMarketOrder) -> None:
        raise NotImplementedError()


class MovingAverageSignalExecutor(SignalExecutor):
    def __init__(self, services: AsyncServices, state: MovingAverageStrategyState):
        super().__init__(services)
        self._services = services
        self._state = state

    @singledispatchmethod
    def execute(self, signal: Signal) -> None:
        raise UnknownSignal()

    @execute.register
    def execute_open_long_market_order(self, signal: OpenLongMarketOrder) -> None:
        self._execute_open_long_market_order(signal)
        self._state._long_open = True
        self._state._position = signal.lots

    @execute.register
    def execute_close_long_market_order(self, signal: CloseLongMarketOrder) -> None:
        self._execute_close_long_market_order(signal)
        self._state._long_open = False
        self._state._position = 0

    @execute.register
    def execute_open_short_market_order(self, signal: OpenShortMarketOrder) -> None:
        self._execute_open_short_market_order(signal)
        self._state._short_open = True
        self._state._position = signal.lots

    @execute.register
    def execute_close_short_market_order(self, signal: CloseShortMarketOrder) -> None:
        self._execute_close_short_market_order(signal)
        self._state._short_open = False
        self._state._position = 0
