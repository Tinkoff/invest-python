from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.signal import (
    CloseLongMarketOrder,
    CloseShortMarketOrder,
    OpenLongMarketOrder,
    OpenShortMarketOrder,
)
from tinkoff.invest.strategies.base.signal_executor_interface import ISignalExecutor


class SignalExecutor(ISignalExecutor):
    def __init__(
        self,
        services: Services,
    ):
        self._services = services

    def execute_open_long_market_order(self, signal: OpenLongMarketOrder) -> None:
        raise NotImplementedError()

    def execute_close_long_market_order(self, signal: CloseLongMarketOrder) -> None:
        raise NotImplementedError()

    def execute_open_short_market_order(self, signal: OpenShortMarketOrder) -> None:
        raise NotImplementedError()

    def execute_close_short_market_order(self, signal: CloseShortMarketOrder) -> None:
        raise NotImplementedError()
