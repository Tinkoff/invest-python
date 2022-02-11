import abc
import asyncio
import logging
from datetime import datetime, timedelta
from typing import AsyncIterator, Iterable, List

import tinkoff
from tinkoff.invest import (
    CandleInstrument,
    HistoricCandle,
    MarketDataRequest,
    MarketDataResponse,
    SubscribeCandlesRequest,
    SubscriptionAction,
)
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.strategies.errors import MarginalTradeIsNotActive, NotEnoughData
from tinkoff.invest.strategies.models import Candle, CandleEvent
from tinkoff.invest.strategies.signal_executor import SignalExecutor
from tinkoff.invest.strategies.strategy import (
    InvestStrategy,
    MovingAverageStrategy,
    MovingAverageStrategySettings,
    MovingAverageStrategyState,
    StrategySettings,
)
from tinkoff.invest.utils import (
    candle_interval_to_subscription_interval,
    quotation_to_decimal,
)

logger = logging.getLogger(__name__)


class ITrader(abc.ABC):
    @abc.abstractmethod
    def trade(self):
        pass


class Trader(ITrader, abc.ABC):
    def __init__(
        self,
        strategy: InvestStrategy,
        services: AsyncServices,
        settings: StrategySettings,
    ):
        self._strategy = strategy
        self._services = services
        self._settings = settings

    @staticmethod
    def _convert_historic_candles_into_candle_events(
        historic_candles: Iterable[HistoricCandle],
    ) -> Iterable[CandleEvent]:
        for candle in historic_candles:
            yield CandleEvent(
                candle=Candle(
                    open=quotation_to_decimal(candle.open),
                    close=quotation_to_decimal(candle.close),
                    high=quotation_to_decimal(candle.high),
                    low=quotation_to_decimal(candle.low),
                ),
                volume=candle.volume,
                time=candle.time,
                is_complete=candle.is_complete,
            )

    def _load_candles(self, period: timedelta) -> Iterable[CandleEvent]:
        logger.info("Loading candles for period %s", period)
        yield from self._services.get_all_candles(
            figi=self._settings.share_id,  # todo ask: figi == share_id?
            from_=datetime.utcnow() - period,
            interval=self._settings.candle_interval,
        )

    @staticmethod
    def _convert_candle(candle: tinkoff.invest.schemas.Candle) -> CandleEvent:
        return CandleEvent(
            candle=Candle(
                open=quotation_to_decimal(candle.open),
                close=quotation_to_decimal(candle.close),
                high=quotation_to_decimal(candle.high),
                low=quotation_to_decimal(candle.low),
            ),
            volume=candle.volume,
            time=candle.time,
            is_complete=False,
        )


class MovingAverageStrategyTrader(Trader):
    def __init__(
        self,
        strategy: MovingAverageStrategy,
        settings: MovingAverageStrategySettings,
        services: AsyncServices,
        state: MovingAverageStrategyState,
        signal_executor: SignalExecutor,
    ):
        super().__init__(strategy, services, settings)
        self._settings = settings
        self._strategy = strategy
        self._services = services
        self._data: List[CandleEvent]
        self._market_data_stream: AsyncIterator[MarketDataResponse]
        self._state = state
        self._signal_executor = signal_executor

        self._data = list(
            self._load_candles(self._settings.short_period + self._settings.long_period)
        )
        self._ensure_enough_candles()
        self._ensure_marginal_trade_active()

        self._strategy.fit(self._data)

    def _ensure_enough_candles(self) -> None:
        if (
            len(self._data)
            < self._settings.short_period.days + self._settings.long_period.days
        ):
            raise NotEnoughData()
        logger.info("Got enough data for strategy")

    @staticmethod
    def _ensure_marginal_trade_active() -> None:
        if False:  # todo ask: how to check?
            raise MarginalTradeIsNotActive()
        logger.info("Marginal trade is active")

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
        self._market_data_stream = self._services.market_data_stream.market_data_stream(
            [candle_subscribe_request]
        ).__aiter__()

    @staticmethod
    def _is_candle_fresh(candle: tinkoff.invest.Candle) -> bool:
        is_fresh_border = datetime.now() - timedelta(seconds=5)
        return candle.time > is_fresh_border

    def _refresh_data(self) -> None:
        try:
            while True:
                market_data_response: MarketDataResponse = (
                    await self._market_data_stream.__anext__()
                )
                candle = market_data_response.candle
                self._strategy.observe(self._convert_candle(candle))
                if self._is_candle_fresh(candle):
                    break
        except asyncio.futures.TimeoutError:
            logger.info("Fresh quotations loaded")
            return

    def trade(self) -> None:
        """Следует стратегии пока не остается вне позиции."""

        while True:
            self._refresh_data()

            signals = self._strategy.predict()
            logger.info("Got signals")
            for signal in signals:
                logger.info("Trying to execute signal %s", signal)
                self._signal_executor.execute(signal)

            if self._state.position == 0:
                logger.info("Strategy run complete")
                return
