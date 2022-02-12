from datetime import datetime, timedelta
from typing import Callable, Iterable, List

import numpy as np

from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.base.errors import CandleEventForDateNotFound
from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal import (
    CloseLongMarketOrder,
    OpenLongMarketOrder,
    OpenShortMarketOrder,
    Signal,
)
from tinkoff.invest.strategies.base.strategy_interface import InvestStrategy
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)
from tinkoff.invest.utils import now


class MovingAverageStrategy(InvestStrategy):
    def __init__(
        self,
        settings: MovingAverageStrategySettings,
        account_manager: AccountManager,
        state: MovingAverageStrategyState,
    ):
        self._data: List[CandleEvent] = []
        self._settings = settings
        self._account_manager = account_manager

        self._state = state
        self._MA_LONG_START: float

    def fit(self, candles: Iterable[CandleEvent]) -> None:
        self._data.extend(candles)

    def observe(self, candle: CandleEvent) -> None:
        self._data.append(candle)

    @staticmethod
    def _get_newer_than_datetime_predicate(
        anchor: datetime,
    ) -> Callable[[CandleEvent], bool]:
        def _(event: CandleEvent) -> bool:
            return event.time > anchor

        return _

    def _filter_from_the_end_with_early_stop(
        self, predicate: Callable[[CandleEvent], bool]
    ) -> Iterable[CandleEvent]:
        for event in reversed(self._data):
            if not predicate(event):
                break
            yield event

    def _select_for_period(self, period: timedelta):
        predicate = self._get_newer_than_datetime_predicate(now() - period)
        return self._filter_from_the_end_with_early_stop(predicate)

    @staticmethod
    def _get_prices(events: Iterable[CandleEvent]) -> Iterable[float]:
        for event in events:
            yield float(event.candle.close)

    def _calculate_moving_average(self, period: timedelta) -> float:
        prices = self._get_prices(self._select_for_period(period))
        return np.mean(prices, axis=0)

    def _calculate_std(self, period: timedelta) -> float:
        prices = self._get_prices(self._select_for_period(period))
        return np.std(prices, axis=0)

    def _get_first_before(self, date: datetime) -> CandleEvent:
        predicate = self._get_newer_than_datetime_predicate(date)
        for event in reversed(self._data):
            if not predicate(event):
                return event
        raise CandleEventForDateNotFound()

    def _init_MA_LONG_START(self):
        date = now() - self._settings.short_period
        event = self._get_first_before(date)
        self._MA_LONG_START = float(event.candle.close)

    def predict(self) -> Iterable[Signal]:  # noqa: C901
        self._init_MA_LONG_START()
        MA_LONG_START = self._MA_LONG_START
        PRICE = float(self._data[-1].candle.close)
        MA_LONG = self._calculate_moving_average(self._settings.long_period)
        MA_SHORT = self._calculate_moving_average(self._settings.short_period)
        STD = self._calculate_std(self._settings.std_period)
        MONEY = float(self._account_manager.get_current_balance())

        if not self._state.long_open:
            if (
                MA_SHORT > MA_LONG
                and abs((PRICE - MA_LONG) / MA_LONG) < STD
                and MA_LONG < MA_LONG_START
            ):
                yield OpenLongMarketOrder(lots=int(MONEY // PRICE))

        if not self._state.short_open:
            if (
                MA_SHORT < MA_LONG
                and abs((PRICE - MA_LONG) / MA_LONG) < STD
                and MA_LONG > MA_LONG_START
            ):
                yield OpenShortMarketOrder(lots=int(MONEY // PRICE))

        if self._state.long_open:
            if (
                PRICE > MA_LONG + 10 * STD
                or False  # todo add predicate: есть сигнал на открытие в шорт
                or PRICE < MA_LONG - 3 * STD
            ):
                yield CloseLongMarketOrder(lots=self._state.position)

        if self._state.short_open:
            if (
                PRICE < MA_LONG - 10 * STD
                or False  # todo add predicate: есть сигнал на открытие в лонг
                or PRICE > MA_LONG + 3 * STD
            ):
                yield CloseLongMarketOrder(lots=self._state.position)
