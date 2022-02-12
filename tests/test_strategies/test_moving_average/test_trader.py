import random
from datetime import timedelta
from decimal import Decimal
from typing import List, Callable, Iterable

import pytest

from tinkoff.invest import CandleInterval, Client, GetCandlesResponse, HistoricCandle, \
    Quotation, MarketDataResponse, Candle, SubscriptionInterval
from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.base.signal_executor_base import SignalExecutor
from tinkoff.invest.strategies.moving_average.strategy import MovingAverageStrategy
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)
from tinkoff.invest.strategies.moving_average.trader import MovingAverageStrategyTrader
from tinkoff.invest.typedefs import ShareId
from tinkoff.invest.utils import now, decimal_to_quotation

from random import gauss, seed
from math import sqrt, exp


def create_GBM(s0, mu, sigma):
    """
    Generates a price following a geometric brownian motion process based on the input of the arguments:
    - s0: Asset inital price.
    - mu: Interest rate expressed annual terms.
    - sigma: Volatility expressed annual terms.
    """
    st = s0

    def generate_range(limit: int):
        nonlocal st

        for i in range(limit):
            st *= exp(
                (mu - 0.5 * sigma ** 2) * (1. / 365.) + sigma * sqrt(1. / 365.) * gauss(
                    mu=0, sigma=1))
            yield st

    return generate_range


@pytest.fixture()
def token() -> str:
    return "some"


@pytest.fixture()
def stock_prices_generator() -> Callable[[int], Iterable[float]]:
    return create_GBM(100, 0.1, 0.05)


@pytest.fixture()
def initial_candles(stock_prices_generator: Callable[[int], Iterable[float]]) -> List[HistoricCandle]:
    now_ = now()
    candles = []
    seed(1234)

    for i, st in enumerate(stock_prices_generator(365)):
        quotation = decimal_to_quotation(Decimal(st))
        candle = HistoricCandle(
            open=quotation,
            high=quotation,
            low=quotation,
            close=quotation,
            volume=100,
            time=now_ - timedelta(days=i),
            is_complete=False,
        )
        candles.append(candle)
    return candles


@pytest.fixture()
def services(
    token: str, mocker, initial_candles: List[HistoricCandle], figi: str,
    stock_prices_generator: Callable[[int], Iterable[float]],
) -> Services:
    with Client(token) as services:
        services.market_data = mocker.Mock(wraps=services.market_data)
        services.market_data.get_candles = mocker.Mock()
        services.market_data.get_candles.return_value = GetCandlesResponse(
            candles=initial_candles
        )
        services.market_data_stream = mocker.Mock(wraps=services.market_data_stream)

        responses = []
        for p in stock_prices_generator(100):
            quotation = decimal_to_quotation(Decimal(p))
            response = MarketDataResponse(
                candle=Candle(
                    figi=figi,
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                    open=quotation,
                    high=quotation,
                    low=quotation,
                    close=quotation,
                    volume=100,
                    time=now()
                )
            )
            responses.append(response)

        services.market_data_stream.market_data_stream.return_value = [
            MarketDataResponse(candle=None),
            *responses,
        ]

        yield services


@pytest.fixture()
def account_manager(services: Services) -> AccountManager:
    return AccountManager(services=services)


@pytest.fixture()
def state() -> MovingAverageStrategyState:
    return MovingAverageStrategyState()


@pytest.fixture()
def figi() -> str:
    return "BBG0047315Y7"


@pytest.fixture()
def settings(figi: str) -> MovingAverageStrategySettings:
    return MovingAverageStrategySettings(
        share_id=ShareId(figi),
        max_transaction_price=Decimal(10000),
        candle_interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        long_period=timedelta(days=100),
        short_period=timedelta(days=30),
        std_period=timedelta(days=30),
    )


@pytest.fixture()
def strategy(
    settings: MovingAverageStrategySettings,
    account_manager: AccountManager,
    state: MovingAverageStrategyState,
) -> MovingAverageStrategy:
    return MovingAverageStrategy(
        settings=settings,
        account_manager=account_manager,
        state=state,
    )


@pytest.fixture()
def signal_executor(
    services: Services,
) -> SignalExecutor:
    return SignalExecutor(
        services=services,
    )


@pytest.fixture()
def moving_average_strategy_trader(
    strategy: MovingAverageStrategy,
    settings: MovingAverageStrategySettings,
    services: Services,
    state: MovingAverageStrategyState,
    signal_executor: SignalExecutor,
) -> MovingAverageStrategyTrader:
    return MovingAverageStrategyTrader(
        strategy=strategy,
        settings=settings,
        services=services,
        state=state,
        signal_executor=signal_executor,
    )


class TestMovingAverageStrategyTrader:
    def test_trade(self, moving_average_strategy_trader: MovingAverageStrategyTrader):
        moving_average_strategy_trader.trade()
