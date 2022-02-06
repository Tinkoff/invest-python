import abc
import dataclasses
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, Iterable, List

import numpy as np

from tinkoff.invest import CandleInterval
from tinkoff.invest._grpc_helpers import Service
from tinkoff.invest.strategy.errors import CandleEventForDateNotFound
from tinkoff.invest.strategy.models import CandleEvent
from tinkoff.invest.strategy.signal import (
    CloseLongMarketOrder,
    OpenLongMarketOrder,
    OpenShortMarketOrder,
    Signal,
)
from tinkoff.invest.typedefs import ShareId


class InvestStrategy(abc.ABC):
    @abc.abstractmethod
    def fit(self, candles: Iterable[CandleEvent]) -> None:
        pass

    @abc.abstractmethod
    def observe(self, candle: CandleEvent) -> None:
        pass

    @abc.abstractmethod
    def predict(self) -> Iterable[Signal]:
        pass


@dataclasses.dataclass
class StrategySettings:
    share_id: ShareId
    max_transaction_price: Decimal
    candle_interval: CandleInterval


@dataclasses.dataclass
class MovingAverageStrategySettings(StrategySettings):
    long_period: timedelta
    short_period: timedelta
    std_period: timedelta


class AccountManager:
    def __init__(self, service: Service):
        self._service = service

    def get_current_balance(self) -> Decimal:
        raise NotImplementedError()


class MovingAverageStrategyState:
    def __init__(self):
        self._long_open: bool = False
        self._short_open: bool = False
        self._position: int = 0

    @property
    def long_open(self) -> bool:
        return self._long_open

    @property
    def short_open(self) -> bool:
        return self._short_open

    @property
    def position(self) -> int:
        return self._position


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
        predicate = self._get_newer_than_datetime_predicate(datetime.now() - period)
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
        date = datetime.now() - self._settings.short_period
        event = self._get_first_before(date)
        self._MA_LONG_START = float(event.candle.close)

    def predict(self) -> Iterable[Signal]:
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
