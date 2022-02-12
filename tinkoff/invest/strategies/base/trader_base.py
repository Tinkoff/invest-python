import abc
from datetime import datetime, timedelta
from typing import Iterable

import tinkoff
from tinkoff.invest import HistoricCandle
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.strategies.base.models import Candle, CandleEvent
from tinkoff.invest.strategies.base.strategy_interface import InvestStrategy
from tinkoff.invest.strategies.base.strategy_settings_base import StrategySettings
from tinkoff.invest.strategies.base.trader_interface import ITrader
from tinkoff.invest.strategies.moving_average.trader import logger
from tinkoff.invest.utils import quotation_to_decimal


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
