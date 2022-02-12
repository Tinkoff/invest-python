import asyncio
import logging
from datetime import timedelta
from typing import Iterator, List

import tinkoff
from tinkoff.invest import (
    CandleInstrument,
    MarketDataRequest,
    MarketDataResponse,
    SubscribeCandlesRequest,
    SubscriptionAction,
)
from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal_executor_base import SignalExecutor
from tinkoff.invest.strategies.base.trader_base import Trader
from tinkoff.invest.strategies.moving_average.strategy import MovingAverageStrategy
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)
from tinkoff.invest.utils import candle_interval_to_subscription_interval, now

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

        self._data = list(
            self._load_candles(self._settings.short_period + self._settings.long_period)
        )
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
        self._market_data_stream = iter(
            self._services.market_data_stream.market_data_stream(
                [candle_subscribe_request]
            )
        )

    @staticmethod
    def _is_candle_fresh(candle: tinkoff.invest.Candle) -> bool:
        is_fresh_border = now() - timedelta(seconds=5)
        logger.debug(
            "Checking if candle is fresh: candle.time=%s > is_fresh_border=%s  %s)",
            candle.time,
            is_fresh_border,
            candle.time > is_fresh_border,
        )
        return candle.time > is_fresh_border

    def _make_observations(self) -> None:
        while True:
            market_data_response: MarketDataResponse = next(self._market_data_stream)
            logger.debug("got market_data_response: %s", market_data_response)
            if market_data_response.candle is None:
                logger.debug("market_data_response didn't have candle")
                continue
            candle = market_data_response.candle
            logger.debug("candle extracted: %s", candle)
            self._strategy.observe(self._convert_candle(candle))
            if self._is_candle_fresh(candle):
                logger.info("Data refreshed")
                break

    def _refresh_data(self) -> None:
        logger.info("Refreshing data")
        try:
            self._make_observations()
        except asyncio.TimeoutError:
            logger.info("Fresh quotations loaded")
            return

    def trade(self) -> None:
        """Следует стратегии пока не остается вне позиции."""

        while True:
            self._refresh_data()

            signals = self._strategy.predict()
            for signal in signals:
                logger.info("Trying to execute signal %s", signal)
                self._signal_executor.execute(signal)

            if self._state.position == 0:
                logger.info("Strategy run complete")
                return
