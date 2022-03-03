import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from decimal import Decimal
from functools import cached_property
from typing import Any, Callable, Dict, Generator, List, Optional

from grpc import Channel
from pytest_freezegun import freeze_time

from tinkoff.invest import (
    Candle,
    GetCandlesResponse,
    GetMarginAttributesResponse,
    HistoricCandle,
    MarketDataResponse,
    MoneyValue,
    OrderDirection,
    OrderType,
    PortfolioPosition,
    PortfolioResponse,
    Quotation,
)
from tinkoff.invest.channels import create_channel
from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.strategy_settings_base import StrategySettings
from tinkoff.invest.typedefs import ChannelArgumentType
from tinkoff.invest.utils import (
    candle_interval_to_subscription_interval,
    decimal_to_quotation,
    now,
    quotation_to_decimal,
)

logger = logging.getLogger(__name__)


@contextmanager
def MockedClient(
    token: str,
    *,
    settings: StrategySettings,
    real_market_data_test_from: datetime,
    real_market_data_test_start: datetime,
    real_market_data_test_end: datetime,
    balance: MoneyValue,
    options: Optional[ChannelArgumentType] = None,
) -> Generator[Services, None, None]:
    with create_channel(options=options) as channel:
        with freeze_time(real_market_data_test_start) as frozen_datetime:
            yield MockedServices(
                channel=channel,
                token=token,
                settings=settings,
                frozen_datetime=frozen_datetime,
                real_market_data_test_from=real_market_data_test_from,
                real_market_data_test_start=real_market_data_test_start,
                real_market_data_test_end=real_market_data_test_end,
                balance=balance,
            )


class MockedServices(Services):
    def __init__(
        self,
        channel: Channel,
        token: str,
        settings: StrategySettings,
        frozen_datetime,
        real_market_data_test_from: datetime,
        real_market_data_test_start: datetime,
        real_market_data_test_end: datetime,
        balance: MoneyValue,
    ):
        super().__init__(channel, token)
        self._settings = settings
        self._figi = settings.share_id
        self._current_market_data: List[Candle] = []
        self._portfolio_positions: Dict[str, PortfolioPosition] = {}
        self._real_market_data_test_from = real_market_data_test_from
        self._real_market_data_test_start = real_market_data_test_start
        self._real_market_data_test_end = real_market_data_test_end
        self._balance = balance
        self._frozen_datetime = frozen_datetime

        _ = self._real_market_data

        self.market_data.get_candles = self._mocked_market_data_get_candles()
        self.orders.post_order = self._mocked_orders_post_order()
        self.operations.get_portfolio = self._mocked_operations_get_portfolio()
        self.market_data_stream.market_data_stream = self._mocked_market_data_stream()
        self.users.get_margin_attributes = self._mocked_users_get_margin_attributes()

    def _mocked_orders_post_order(self) -> Callable[[Any], Any]:
        def _post_order(  # pylint: disable=too-many-locals
            *,
            figi: str = "",
            quantity: int = 0,
            price: Optional[Quotation] = None,  # pylint: disable=unused-argument
            direction: OrderDirection = OrderDirection(0),
            account_id: str = "",
            order_type: OrderType = OrderType(0),
            order_id: str = "",  # pylint: disable=unused-argument
        ):
            assert figi == self._settings.share_id
            assert quantity > 0
            assert account_id == self._settings.account_id
            assert order_type.ORDER_TYPE_MARKET

            last_candle = self._current_market_data[-1]
            last_market_price = quotation_to_decimal(last_candle.close)

            position = self._portfolio_positions.get(figi)
            if position is None:
                position = PortfolioPosition(
                    figi=figi,
                    quantity=decimal_to_quotation(Decimal(0)),
                )

            if direction == OrderDirection.ORDER_DIRECTION_SELL:
                quantity_delta = -quantity
                balance_delta = last_market_price * quantity
            elif direction == OrderDirection.ORDER_DIRECTION_BUY:
                quantity_delta = +quantity
                balance_delta = -(last_market_price * quantity)

            else:
                raise AssertionError("Incorrect direction")

            logger.warning("Operation: %s, %s", direction, balance_delta)

            old_quantity = quotation_to_decimal(position.quantity)
            new_quantity = decimal_to_quotation(old_quantity + quantity_delta)

            position.quantity.units = new_quantity.units
            position.quantity.nano = new_quantity.nano

            old_balance = quotation_to_decimal(
                Quotation(units=self._balance.units, nano=self._balance.nano)
            )
            new_balance = decimal_to_quotation(old_balance + balance_delta)

            self._balance.units = new_balance.units
            self._balance.nano = new_balance.nano

            self._portfolio_positions[figi] = position

        return _post_order  # type: ignore

    @cached_property
    def _portfolio_response(self) -> PortfolioResponse:
        return PortfolioResponse(
            total_amount_shares=MoneyValue(currency="rub", units=28691, nano=300000000),
            total_amount_bonds=MoneyValue(currency="rub", units=0, nano=0),
            total_amount_etf=MoneyValue(currency="rub", units=0, nano=0),
            total_amount_currencies=self._balance,
            total_amount_futures=MoneyValue(currency="rub", units=0, nano=0),
            expected_yield=Quotation(units=0, nano=-350000000),
            positions=list(self._portfolio_positions.values()),
        )

    def _mocked_operations_get_portfolio(self) -> Callable[[Any], Any]:
        def _get_portfolio(*args, **kwars):  # pylint: disable=unused-argument
            return self._portfolio_response

        return _get_portfolio

    def _mocked_market_data_stream(self) -> Callable[[Any], Any]:
        self._frozen_datetime.move_to(self._real_market_data_test_start)

        def _market_data_stream(*args, **kwargs):  # pylint: disable=unused-argument
            yield MarketDataResponse(candle=None)  # type: ignore

            interval = candle_interval_to_subscription_interval(
                self._settings.candle_interval
            )
            for historic_candle in self._after_start_candles:
                candle = Candle(
                    figi=self._figi,
                    interval=interval,
                    open=historic_candle.open,
                    high=historic_candle.high,
                    low=historic_candle.low,
                    close=historic_candle.close,
                    volume=historic_candle.volume,
                    time=historic_candle.time,
                )
                self._current_market_data.append(candle)
                yield MarketDataResponse(candle=candle)
                self._frozen_datetime.move_to(now() + timedelta(minutes=1))

        return _market_data_stream

    @cached_property
    def _real_market_data(self) -> List[HistoricCandle]:
        real_market_data = []
        for candle in self.get_all_candles(
            figi=self._figi,
            from_=self._real_market_data_test_from,
            to=self._real_market_data_test_end,
            interval=self._settings.candle_interval,
        ):
            real_market_data.append(candle)
        return real_market_data

    @cached_property
    def _initial_candles(self) -> List[HistoricCandle]:
        return [
            candle
            for candle in self._real_market_data
            if candle.time < self._real_market_data_test_start
        ]

    @cached_property
    def _after_start_candles(self) -> List[HistoricCandle]:
        return [
            candle
            for candle in self._real_market_data
            if candle.time >= self._real_market_data_test_start
        ]

    def _mocked_market_data_get_candles(self):
        def _get_candles(*args, **kwargs):  # pylint: disable=unused-argument
            return GetCandlesResponse(candles=self._initial_candles)

        return _get_candles

    def _mocked_users_get_margin_attributes(self):
        def _get_margin_attributes(*agrs, **kwargs):  # pylint: disable=unused-argument
            return GetMarginAttributesResponse(
                liquid_portfolio=MoneyValue(currency="", units=0, nano=0),
                starting_margin=MoneyValue(currency="", units=0, nano=0),
                minimal_margin=MoneyValue(currency="", units=0, nano=0),
                funds_sufficiency_level=Quotation(units=322, nano=0),
                amount_of_missing_funds=MoneyValue(currency="", units=0, nano=0),
            )

        return _get_margin_attributes
