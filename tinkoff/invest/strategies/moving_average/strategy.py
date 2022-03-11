import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, Iterable, List

import numpy as np

from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.base.errors import (
    CandleEventForDateNotFound,
    NotEnoughData,
    OldCandleObservingError,
)
from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal import (
    CloseLongMarketOrder,
    CloseShortMarketOrder,
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
from tinkoff.invest.utils import (
    candle_interval_to_timedelta,
    ceil_datetime,
    floor_datetime,
    now,
)

logger = logging.getLogger(__name__)


class MovingAverageStrategy(InvestStrategy):
    def __init__(
        self,
        settings: MovingAverageStrategySettings,
        account_manager: AccountManager,
        state: MovingAverageStrategyState,
    ):
        super().__init__()
        self._data: List[CandleEvent] = []
        self._settings = settings
        self._account_manager = account_manager

        self._state = state
        self._MA_LONG_START: Decimal
        self._candle_interval_timedelta = candle_interval_to_timedelta(
            self._settings.candle_interval
        )

    def _ensure_enough_candles(self) -> None:
        date = now() - (self._settings.short_period + self._settings.long_period) #фикс на использование периодов
        try:
            self._get_first_candle_before(date)
        except CandleEventForDateNotFound as e:
            raise NotEnoughData() from e
        logger.info("Got enough data for strategy")

    def fit(self, candles: Iterable[CandleEvent]) -> None:
        logger.debug("Strategy fitting with candles %s", candles)
        for candle in candles:
            self.observe(candle)
        self._ensure_enough_candles()

    def _append_candle_event(self, candle_event: CandleEvent) -> None:
        last_candle_event = self._data[-1]
        last_interval_floor = floor_datetime(
            last_candle_event.time, self._candle_interval_timedelta
        )
        last_interval_ceil = ceil_datetime(
            last_candle_event.time, self._candle_interval_timedelta
        )

        if candle_event.time < last_interval_floor:
            raise OldCandleObservingError()
        if candle_event.time < last_interval_ceil:
            self._data[-1] = candle_event
        else:
            self._data.append(candle_event)

    def observe(self, candle: CandleEvent) -> None:
        logger.debug("Observing candle event: %s", candle)

        if len(self._data) > 0:
            self._append_candle_event(candle)
        else:
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
    def _get_prices(events: Iterable[CandleEvent]) -> Iterable[Decimal]:
        for event in events:
            yield event.candle.close

    def _calculate_moving_average(self, period: timedelta) -> Decimal:
        prices = list(self._get_prices(self._select_for_period(period)))
        logger.debug("Selected prices: %s", prices)
        return np.mean(prices, axis=0)  # type: ignore

    def _calculate_std(self, period: timedelta) -> Decimal:
        prices = list(self._get_prices(self._select_for_period(period)))
        return np.std(prices, axis=0)  # type: ignore

    def _get_first_candle_before(self, date: datetime) -> CandleEvent:
        predicate = self._get_newer_than_datetime_predicate(date)
        for event in reversed(self._data):
            if not predicate(event):
                return event
        raise CandleEventForDateNotFound()

    def _init_MA_LONG_START(self):
        date = now() - self._settings.short_period
        event = self._get_first_candle_before(date)
        self._MA_LONG_START = event.candle.close

    @staticmethod
    def _is_long_open_signal(
        MA_SHORT: Decimal,
        MA_LONG: Decimal,
        PRICE: Decimal,
        STD: Decimal,
        MA_LONG_START: Decimal,
    ) -> bool:
        logger.debug("Try long opening")
        logger.debug("\tMA_SHORT > MA_LONG, %s", MA_SHORT > MA_LONG)
        logger.debug(
            "\tand abs((PRICE - MA_LONG) / MA_LONG) < STD, %s",
            abs((PRICE - MA_LONG) / MA_LONG) < STD,
        )
        logger.debug("\tand MA_LONG < MA_LONG_START, %s", MA_LONG > MA_LONG_START)
        logger.debug(
            "== %s",
            MA_SHORT > MA_LONG
            and abs((PRICE - MA_LONG) / MA_LONG) < STD
            and MA_LONG > MA_LONG_START, #сравниваем MA_LONG с MA_LONG self._settings.short_period/2 назад
        )
        return (
            MA_SHORT > MA_LONG
            and abs((PRICE - MA_LONG) / MA_LONG) < STD
            and MA_LONG > MA_LONG_START
        )

    @staticmethod
    def _is_short_open_signal(
        MA_SHORT: Decimal,
        MA_LONG: Decimal,
        PRICE: Decimal,
        STD: Decimal,
        MA_LONG_START: Decimal,
    ) -> bool:
        logger.debug("Try short opening")
        logger.debug("\tMA_SHORT < MA_LONG, %s", MA_SHORT < MA_LONG)
        logger.debug(
            "\tand abs((PRICE - MA_LONG) / MA_LONG) < STD, %s",
            abs((PRICE - MA_LONG) / MA_LONG) < STD,
        )
        logger.debug("\tand MA_LONG > MA_LONG_START, %s", MA_LONG < MA_LONG_START)
        logger.debug(
            "== %s",
            MA_SHORT < MA_LONG
            and abs((PRICE - MA_LONG) / MA_LONG) < STD
            and MA_LONG < MA_LONG_START,
        )
        return (
            MA_SHORT < MA_LONG
            and abs((PRICE - MA_LONG) / MA_LONG) < STD
            and MA_LONG < MA_LONG_START
        )

    @staticmethod
    def _is_long_close_signal(
        MA_LONG: Decimal,
        PRICE: Decimal,
        STD: Decimal,
        has_short_open_signal: bool,
    ) -> bool:
        logger.debug("Try long closing")
        logger.debug("\tPRICE > MA_LONG + 10 * STD, %s", PRICE > MA_LONG + 10 * STD)
        logger.debug("\tor has_short_open_signal, %s", has_short_open_signal)
        logger.debug("\tor PRICE < MA_LONG - 3 * STD, %s", PRICE < MA_LONG - 3 * STD)
        logger.debug(
            "== %s",
            PRICE > MA_LONG + 10 * STD
            or has_short_open_signal
            or PRICE < MA_LONG - 3 * STD,
        )
        return (
            PRICE > MA_LONG + 10 * STD
            or has_short_open_signal
            or PRICE < MA_LONG - 3 * STD
        )

    @staticmethod
    def _is_short_close_signal(
        MA_LONG: Decimal,
        PRICE: Decimal,
        STD: Decimal,
        has_long_open_signal: bool,
    ) -> bool:
        logger.debug("Try short closing")
        logger.debug("\tPRICE < MA_LONG - 10 * STD, %s", PRICE < MA_LONG - 10 * STD)
        logger.debug("\tor has_long_open_signal, %s", has_long_open_signal)
        logger.debug("\tor PRICE > MA_LONG + 3 * STD, %s", PRICE > MA_LONG + 3 * STD)
        logger.debug(
            "== %s",
            PRICE < MA_LONG - 10 * STD #кажется, что не работает закрытие
            or has_long_open_signal
            or PRICE > MA_LONG + 3 * STD,
        )
        return (
            PRICE < MA_LONG - 10 * STD
            or has_long_open_signal
            or PRICE > MA_LONG + 3 * STD
        )

    def predict(self) -> Iterable[Signal]:  # noqa: C901
        logger.info("Strategy predict")
        self._init_MA_LONG_START()
        MA_LONG_START = self._MA_LONG_START
        logger.debug("MA_LONG_START: %s", MA_LONG_START)
        PRICE = self._data[-1].candle.close
        logger.debug("PRICE: %s", PRICE)
        MA_LONG = self._calculate_moving_average(self._settings.long_period)
        logger.debug("MA_LONG: %s", MA_LONG)
        MA_SHORT = self._calculate_moving_average(self._settings.short_period)
        logger.debug("MA_SHORT: %s", MA_SHORT)
        STD = self._calculate_std(self._settings.std_period)
        logger.debug("STD: %s", STD)
        MONEY = self._account_manager.get_current_balance()
        logger.debug("MONEY: %s", MONEY)

        has_long_open_signal = False
        has_short_open_signal = False

        possible_lots = int(MONEY // PRICE)

        if (
            not self._state.long_open
            and self._is_long_open_signal(
                MA_SHORT=MA_SHORT,
                MA_LONG=MA_LONG,
                PRICE=PRICE,
                STD=STD,
                MA_LONG_START=MA_LONG_START,
            )
            and possible_lots > 0
        ):
            has_long_open_signal = True
            yield OpenLongMarketOrder(lots=possible_lots)

        if (
            not self._state.short_open
            and self._is_short_open_signal(
                MA_SHORT=MA_SHORT,
                MA_LONG=MA_LONG,
                PRICE=PRICE,
                STD=STD,
                MA_LONG_START=MA_LONG_START,
            )
            and possible_lots > 0
        ):
            has_short_open_signal = True
            yield OpenShortMarketOrder(lots=possible_lots)

        if self._state.long_open and self._is_long_close_signal(
            MA_LONG=MA_LONG,
            PRICE=PRICE,
            STD=STD,
            has_short_open_signal=has_short_open_signal,
        ):
            yield CloseLongMarketOrder(lots=self._state.position)

        if self._state.short_open and self._is_short_close_signal(
            MA_LONG=MA_LONG,
            PRICE=PRICE,
            STD=STD,
            has_long_open_signal=has_long_open_signal,
        ):
            yield CloseShortMarketOrder(lots=self._state.position)
