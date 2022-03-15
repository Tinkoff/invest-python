import logging
import time
from datetime import timedelta
from typing import Iterator, List

import tinkoff
from tinkoff.invest import (
    CandleInstrument,
    InvestError,
    MarketDataRequest,
    MarketDataResponse,
    SubscribeCandlesRequest,
    SubscriptionAction,
)
from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.base.errors import MarketDataNotAvailableError
from tinkoff.invest.strategies.base.event import DataEvent, SignalEvent
from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal import CloseSignal, OpenSignal, Signal
from tinkoff.invest.strategies.base.signal_executor_base import SignalExecutor
from tinkoff.invest.strategies.base.trader_base import Trader
from tinkoff.invest.strategies.moving_average.strategy import MovingAverageStrategy
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)
from tinkoff.invest.strategies.moving_average.supervisor import (
    MovingAverageStrategySupervisor,
)
from tinkoff.invest.utils import candle_interval_to_subscription_interval, now, \
    floor_datetime

logger = logging.getLogger(__name__)


class MovingAverageStrategyTrader(Trader):
    def __init__(
        self,
        strategy: MovingAverageStrategy,
        settings: MovingAverageStrategySettings,
        services: Services,
        state: MovingAverageStrategyState,
        signal_executor: SignalExecutor,
        account_manager: AccountManager,
        supervisor: MovingAverageStrategySupervisor,
    ):
        super().__init__(strategy, services, settings)
        self._settings: MovingAverageStrategySettings = settings
        self._strategy = strategy
        self._services = services
        self._data: List[CandleEvent]
        self._market_data_stream: Iterator[MarketDataResponse]
        self._state = state
        self._signal_executor = signal_executor
        self._account_manager = account_manager
        self._supervisor = supervisor

        self._data = list(
            self._load_candles(self._settings.short_period + self._settings.long_period)
        )
        for candle_event in self._data:
            self._supervisor.notify(self._convert_to_data_event(candle_event))
        self._ensure_marginal_trade_active()

        self._subscribe()

        self._strategy.fit(self._data)

    def _ensure_marginal_trade_active(self) -> None:
        self._account_manager.ensure_marginal_trade()

    def _subscribe(self):
        current_instrument = CandleInstrument(
            figi=self._settings.share_id,
            interval=candle_interval_to_subscription_interval(
                self._settings.candle_interval
            ),
        )
        candle_subscribe_request = MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[current_instrument],
            )
        )

        def request_iterator():
            yield candle_subscribe_request
            while True:
                time.sleep(1)

        self._market_data_stream = self._services.market_data_stream.market_data_stream(
            request_iterator()
        )

    def _is_candle_fresh(self, candle: tinkoff.invest.Candle) -> bool:
        is_fresh_border = floor_datetime(
            now(),
            delta=self._settings.candle_interval_timedelta
        )
        logger.debug(
            "Checking if candle is fresh: candle.time=%s > is_fresh_border=%s  %s)",
            candle.time,
            is_fresh_border,
            candle.time >= is_fresh_border,
        )
        return candle.time >= is_fresh_border

    @staticmethod
    def _convert_to_data_event(candle_event: CandleEvent) -> DataEvent:
        return DataEvent(candle_event=candle_event, time=candle_event.time)

    def _make_observations(self) -> None:
        while True:
            market_data_response: MarketDataResponse = next(self._market_data_stream)
            logger.debug("got market_data_response: %s", market_data_response)
            if market_data_response.candle is None:
                logger.debug("market_data_response didn't have candle")
                continue
            candle = market_data_response.candle
            logger.debug("candle extracted: %s", candle)
            candle_event = self._convert_candle(candle)
            self._strategy.observe(candle_event)
            self._supervisor.notify(self._convert_to_data_event(candle_event))
            if self._is_candle_fresh(candle):
                logger.info("Data refreshed")
                break

    def _refresh_data(self) -> None:
        logger.info("Refreshing data")
        try:
            self._make_observations()
        except StopIteration as e:
            logger.info("Fresh quotations not available")
            raise MarketDataNotAvailableError() from e

    def _filter_closing_signals(self, signals: List[Signal]) -> List[Signal]:
        return list(filter(lambda signal: isinstance(signal, CloseSignal), signals))

    def _filter_opening_signals(self, signals: List[Signal]) -> List[Signal]:
        return list(filter(lambda signal: isinstance(signal, OpenSignal), signals))

    def _execute(self, signal: Signal) -> None:
        logger.info("Trying to execute signal %s", signal)
        try:
            self._signal_executor.execute(signal)
        except InvestError:
            was_executed = False
        else:
            was_executed = True
        self._supervisor.notify(
            SignalEvent(signal=signal, was_executed=was_executed, time=now())
        )

    def _get_signals(self) -> List[Signal]:
        signals = list(self._strategy.predict())
        return [
            *self._filter_closing_signals(signals),
            *self._filter_opening_signals(signals),
        ]

    def trade(self) -> None:
        """Делает попытку следовать стратегии."""

        logger.info("Balance: %s", self._account_manager.get_current_balance())
        self._refresh_data()

        signals = self._get_signals()
        if signals:
            logger.info("Got signals %s", signals)
        for signal in signals:
            self._execute(signal)
        if self._state.position == 0:
            logger.info("Trade try complete")
