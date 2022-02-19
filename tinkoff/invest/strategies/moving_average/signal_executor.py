import logging
from functools import singledispatchmethod

from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.errors import UnknownSignal
from tinkoff.invest.strategies.base.signal import (
    CloseLongMarketOrder,
    CloseShortMarketOrder,
    OpenLongMarketOrder,
    OpenShortMarketOrder,
    Signal,
)
from tinkoff.invest.strategies.base.signal_executor_base import SignalExecutor
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)

logger = logging.getLogger(__name__)


class MovingAverageSignalExecutor(SignalExecutor):
    def __init__(
        self,
        services: Services,
        state: MovingAverageStrategyState,
        settings: MovingAverageStrategySettings,
    ):
        super().__init__(services, settings)
        self._services = services
        self._state = state

    @singledispatchmethod
    def execute(self, signal: Signal) -> None:
        raise UnknownSignal()

    @execute.register
    def _execute_open_long_market_order(self, signal: OpenLongMarketOrder) -> None:
        self.execute_open_long_market_order(signal)
        self._state.long_open = True
        self._state.position = signal.lots
        logger.info("Signal executed %s", signal)

    @execute.register
    def _execute_close_long_market_order(self, signal: CloseLongMarketOrder) -> None:
        self.execute_close_long_market_order(signal)
        self._state.long_open = False
        self._state.position = 0
        logger.info("Signal executed %s", signal)

    @execute.register
    def _execute_open_short_market_order(self, signal: OpenShortMarketOrder) -> None:
        self.execute_open_short_market_order(signal)
        self._state.short_open = True
        self._state.position = signal.lots
        logger.info("Signal executed %s", signal)

    @execute.register
    def _execute_close_short_market_order(self, signal: CloseShortMarketOrder) -> None:
        self.execute_close_short_market_order(signal)
        self._state.short_open = False
        self._state.position = 0
        logger.info("Signal executed %s", signal)
