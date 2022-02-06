import abc
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Iterable, List, AsyncIterable, AsyncIterator

import tinkoff

from tinkoff.invest import HistoricCandle, SubscribeCandlesRequest, SubscriptionAction, \
    CandleInstrument, MarketDataRequest, MarketDataResponse
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.services import Services
from tinkoff.invest.strategy.errors import NotEnoughData
from tinkoff.invest.strategy.models import CandleEvent, Candle
from tinkoff.invest.strategy.strategy import MovingAverageStrategySettings, \
    MovingAverageStrategy, InvestStrategy, StrategySettings, MovingAverageStrategyState
from tinkoff.invest.utils import quotation_to_decimal, \
    candle_interval_to_subscription_interval

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
        historic_candles: Iterable[HistoricCandle]
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
                is_complete=candle.is_complete
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
    ):
        super().__init__(strategy, services, settings)
        self._settings = settings
        self._strategy = strategy
        self._services = services
        self._data: List[CandleEvent]
        self._market_data_stream: AsyncIterator[MarketDataResponse]
        self._state = state

        self._data = list(self._load_candles(self._settings.short_period + self._settings.long_period))
        self._ensure_enough_candles()
        self._ensure_marginal_trade_active()

    def _ensure_enough_candles(self) -> None:
        if len(self._data) < self._settings.short_period.days + self._settings.long_period.days:
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
            interval=candle_interval_to_subscription_interval(self._settings.candle_interval),
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


    def _refresh_data(self):

        try:
            while True:
                message = await asyncio.wait_for(
                    self._market_data_stream.__anext__(),
                    timeout=0.1
                )
        except asyncio.futures.TimeoutError:
            # streaming is completed
            pass

    def trade(self) -> None:
        """ Делает один оборот стратегии. После выполнения остается вне позиции. """
        await it.__anext__()