from datetime import timedelta
from decimal import Decimal
from math import exp, sqrt
from random import gauss, seed
from typing import Callable, Iterable, List

import pytest

from tinkoff.invest import (
    Candle,
    CandleInterval,
    Client,
    GetCandlesResponse,
    HistoricCandle,
    MarketDataResponse,
    MoneyValue,
    PortfolioPosition,
    PortfolioResponse,
    Quotation,
    SubscriptionInterval,
)
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
from tinkoff.invest.typedefs import AccountId, ShareId
from tinkoff.invest.utils import decimal_to_quotation, now

seed(1234)


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
                (mu - 0.5 * sigma ** 2) * (1.0 / 365.0)
                + sigma * sqrt(1.0 / 365.0) * gauss(mu=0, sigma=1)
            )
            yield st

    return generate_range


@pytest.fixture()
def token() -> str:
    return "some"


@pytest.fixture()
def stock_prices_generator() -> Callable[[int], Iterable[float]]:
    return create_GBM(100, 0.1, 0.05)


@pytest.fixture()
def initial_candles(
    stock_prices_generator: Callable[[int], Iterable[float]]
) -> List[HistoricCandle]:
    now_ = now()
    candles = []

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
    token: str,
    mocker,
    initial_candles: List[HistoricCandle],
    figi: str,
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
                    time=now(),
                )
            )
            responses.append(response)

        services.market_data_stream.market_data_stream.return_value = [
            MarketDataResponse(candle=None),
            *responses,
        ]

        services.operations = mocker.Mock(wraps=services.operations)
        services.operations.get_portfolio.return_value = PortfolioResponse(
            total_amount_shares=MoneyValue(currency="rub", units=28691, nano=300000000),
            total_amount_bonds=MoneyValue(currency="rub", units=0, nano=0),
            total_amount_etf=MoneyValue(currency="rub", units=0, nano=0),
            total_amount_currencies=MoneyValue(
                currency="rub", units=2005, nano=690000000
            ),
            total_amount_futures=MoneyValue(currency="rub", units=0, nano=0),
            expected_yield=Quotation(units=0, nano=-350000000),
            positions=[
                PortfolioPosition(
                    figi="BBG004730N88",
                    instrument_type="share",
                    quantity=Quotation(units=110, nano=0),
                    average_position_price=MoneyValue(
                        currency="rub", units=261, nano=800000000
                    ),
                    expected_yield=Quotation(units=-106, nano=-700000000),
                    current_nkd=MoneyValue(currency="", units=0, nano=0),
                    average_position_price_pt=Quotation(units=0, nano=0),
                    current_price=MoneyValue(currency="rub", units=260, nano=830000000),
                )
            ],
        )

        yield services


@pytest.fixture()
def account_manager(
    services: Services, settings: MovingAverageStrategySettings
) -> AccountManager:
    return AccountManager(services=services, strategy_settings=settings)


@pytest.fixture()
def state() -> MovingAverageStrategyState:
    return MovingAverageStrategyState()


@pytest.fixture()
def figi() -> str:
    return "BBG0047315Y7"


@pytest.fixture()
def account_id() -> str:
    return AccountId("1337007228")


@pytest.fixture()
def settings(figi: str, account_id: AccountId) -> MovingAverageStrategySettings:
    return MovingAverageStrategySettings(
        share_id=ShareId(figi),
        account_id=account_id,
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
