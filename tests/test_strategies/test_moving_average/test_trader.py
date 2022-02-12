import logging
from datetime import timedelta
from decimal import Decimal
from math import exp, sqrt
from random import gauss, seed
from typing import Callable, Iterable, Iterator, List

import pytest

from tinkoff.invest import (
    Candle,
    CandleInterval,
    Client,
    GetCandlesResponse,
    GetMarginAttributesResponse,
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
from tinkoff.invest.utils import candle_interval_to_timedelta, decimal_to_quotation, now

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

seed(1234)


def create_GBM(s0, mu, sigma) -> Callable[[int], Iterable[float]]:
    """
    Generates a price following a geometric brownian motion process based on the input.
    - s0: Asset initial price.
    - mu: Interest rate expressed annual terms.
    - sigma: Volatility expressed annual terms.
    """
    st = s0

    def generate_range(limit: int):
        nonlocal st

        for _ in range(limit):
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
    settings: MovingAverageStrategySettings,
    stock_prices_generator: Callable[[int], Iterable[float]],
) -> Iterable[HistoricCandle]:
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
            time=now_ - candle_interval_to_timedelta(settings.candle_interval) * i,
            is_complete=False,
        )
        candles.append(candle)
    return reversed(candles)


@pytest.fixture()
def real_services(token: str) -> Iterator[Services]:
    with Client(token) as services:
        yield services


@pytest.fixture()
def mock_market_data_service(
    real_services: Services,
    mocker,
    initial_candles: List[HistoricCandle],
) -> Services:
    real_services.market_data = mocker.Mock(wraps=real_services.market_data)

    real_services.market_data.get_candles = mocker.Mock()
    real_services.market_data.get_candles.return_value = GetCandlesResponse(
        candles=initial_candles
    )

    return real_services


@pytest.fixture()
def mock_market_data_stream_service(
    real_services: Services,
    mocker,
    figi: str,
    stock_prices_generator: Callable[[int], Iterable[float]],
) -> Services:
    real_services.market_data_stream = mocker.Mock(
        wraps=real_services.market_data_stream
    )
    responses = []
    for price in stock_prices_generator(100):
        quotation = decimal_to_quotation(Decimal(price))
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

    real_services.market_data_stream.market_data_stream.return_value = [
        MarketDataResponse(candle=None),  # type: ignore
        *responses,
    ]

    return real_services


@pytest.fixture()
def mock_operations_service(
    real_services: Services,
    mocker,
) -> Services:
    real_services.operations = mocker.Mock(wraps=real_services.operations)
    real_services.operations.get_portfolio.return_value = PortfolioResponse(
        total_amount_shares=MoneyValue(currency="rub", units=28691, nano=300000000),
        total_amount_bonds=MoneyValue(currency="rub", units=0, nano=0),
        total_amount_etf=MoneyValue(currency="rub", units=0, nano=0),
        total_amount_currencies=MoneyValue(currency="rub", units=2005, nano=690000000),
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

    return real_services


@pytest.fixture()
def mock_users_service(
    real_services: Services,
    mocker,
) -> Services:
    real_services.users = mocker.Mock(wraps=real_services.users)
    real_services.users.get_margin_attributes.return_value = (
        GetMarginAttributesResponse(
            liquid_portfolio=MoneyValue(currency="", units=0, nano=0),
            starting_margin=MoneyValue(currency="", units=0, nano=0),
            minimal_margin=MoneyValue(currency="", units=0, nano=0),
            funds_sufficiency_level=Quotation(units=322, nano=0),
            amount_of_missing_funds=MoneyValue(currency="", units=0, nano=0),
        )
    )

    return real_services


@pytest.fixture()
def mocked_services(
    real_services: Services,
    mock_market_data_service,
    mock_market_data_stream_service,
    mock_operations_service,
    mock_users_service,
) -> Services:
    return real_services


@pytest.fixture()
def account_manager(
    mocked_services: Services, settings: MovingAverageStrategySettings
) -> AccountManager:
    return AccountManager(services=mocked_services, strategy_settings=settings)


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
        long_period=timedelta(hours=100),
        short_period=timedelta(hours=60),
        std_period=timedelta(hours=30),
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
    mocked_services: Services,
) -> SignalExecutor:
    return SignalExecutor(
        services=mocked_services,
    )


@pytest.fixture()
def moving_average_strategy_trader(
    strategy: MovingAverageStrategy,
    settings: MovingAverageStrategySettings,
    mocked_services: Services,
    state: MovingAverageStrategyState,
    signal_executor: SignalExecutor,
    account_manager: AccountManager,
) -> MovingAverageStrategyTrader:
    return MovingAverageStrategyTrader(
        strategy=strategy,
        settings=settings,
        services=mocked_services,
        state=state,
        signal_executor=signal_executor,
        account_manager=account_manager,
    )


class TestMovingAverageStrategyTrader:
    def test_trade(
        self, moving_average_strategy_trader: MovingAverageStrategyTrader, caplog
    ):
        caplog.set_level(logging.DEBUG)

        for i in range(100):
            logger.info("Trade %s", i)
            moving_average_strategy_trader.trade()

        assert 0
