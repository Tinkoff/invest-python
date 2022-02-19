import logging
from datetime import timedelta
from decimal import Decimal
from math import exp, sqrt
from random import gauss, seed
from typing import Callable, Dict, Iterable, Iterator, List, Optional

import pytest
from grpc import StatusCode

from tinkoff.invest import (
    Candle,
    CandleInterval,
    Client,
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
    RequestError,
)
from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.moving_average.plotter import \
    MovingAverageStrategyPlotter
from tinkoff.invest.strategies.moving_average.signal_executor import (
    MovingAverageSignalExecutor,
)
from tinkoff.invest.strategies.moving_average.strategy import MovingAverageStrategy
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)
from tinkoff.invest.strategies.moving_average.supervisor import \
    MovingAverageStrategySupervisor
from tinkoff.invest.strategies.moving_average.trader import MovingAverageStrategyTrader
from tinkoff.invest.strategies.plotting.plotter import StrategyPlotter
from tinkoff.invest.typedefs import AccountId, ShareId
from tinkoff.invest.utils import (
    candle_interval_to_subscription_interval,
    candle_interval_to_timedelta,
    decimal_to_quotation,
    now,
    quotation_to_decimal,
)

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

seed(1338)


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
    return create_GBM(100, 0.01, 0.1)


@pytest.fixture()
def stock_volume_generator() -> Callable[[int], Iterable[float]]:
    return create_GBM(1000, 0.9, 1.1)


@pytest.fixture()
def initial_candles(
    settings: MovingAverageStrategySettings,
    stock_prices_generator: Callable[[int], Iterable[float]],
    stock_volume_generator: Callable[[int], Iterable[float]],
) -> Iterable[HistoricCandle]:
    candles = []
    intervals = 365
    interval_delta = candle_interval_to_timedelta(settings.candle_interval)
    base = now() - interval_delta * intervals
    (close,) = stock_prices_generator(1)
    for i in range(intervals):
        open_ = close
        low, high, close = stock_prices_generator(3)
        low, high = min(low, high, open_, close), max(low, high, open_, close)
        (volume,) = stock_volume_generator(1)
        candle = HistoricCandle(
            open=decimal_to_quotation(Decimal(open_)),
            high=decimal_to_quotation(Decimal(high)),
            low=decimal_to_quotation(Decimal(low)),
            close=decimal_to_quotation(Decimal(close)),
            volume=int(volume),
            time=base + interval_delta * i,
            is_complete=True,
        )
        candles.append(candle)
    return candles


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
def current_market_data() -> List[Candle]:
    return []


@pytest.fixture()
def mock_market_data_stream_service(
    real_services: Services,
    mocker,
    figi: str,
    stock_prices_generator: Callable[[int], Iterable[float]],
    stock_volume_generator: Callable[[int], Iterable[float]],
    settings: MovingAverageStrategySettings,
    current_market_data: List[Candle],
    freezer,
) -> Services:
    real_services.market_data_stream = mocker.Mock(
        wraps=real_services.market_data_stream
    )

    def _market_data_stream(*args, **kwargs):
        yield MarketDataResponse(candle=None)  # type: ignore

        (close,) = stock_prices_generator(1)
        while True:
            open_ = close
            low, high, close = stock_prices_generator(3)
            low, high = min(low, high, open_, close), max(low, high, open_, close)
            (volume,) = stock_volume_generator(1)
            candle = Candle(
                figi=figi,
                interval=candle_interval_to_subscription_interval(
                    settings.candle_interval
                ),
                open=decimal_to_quotation(Decimal(open_)),
                high=decimal_to_quotation(Decimal(high)),
                low=decimal_to_quotation(Decimal(low)),
                close=decimal_to_quotation(Decimal(close)),
                volume=int(volume),
                time=now(),
            )
            current_market_data.append(candle)
            yield MarketDataResponse(candle=candle)
            freezer.move_to(now() + timedelta(minutes=1))

    real_services.market_data_stream.market_data_stream = _market_data_stream

    return real_services


@pytest.fixture()
def portfolio_positions() -> Dict[str, PortfolioPosition]:
    return {
        "BBG004730N88": PortfolioPosition(
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
    }


@pytest.fixture()
def balance() -> MoneyValue:
    return MoneyValue(currency="rub", units=20050, nano=690000000)


@pytest.fixture()
def portfolio_response(
    portfolio_positions: Dict[str, PortfolioPosition],
    balance: MoneyValue,
) -> PortfolioResponse:
    return PortfolioResponse(
        total_amount_shares=MoneyValue(currency="rub", units=28691, nano=300000000),
        total_amount_bonds=MoneyValue(currency="rub", units=0, nano=0),
        total_amount_etf=MoneyValue(currency="rub", units=0, nano=0),
        total_amount_currencies=balance,
        total_amount_futures=MoneyValue(currency="rub", units=0, nano=0),
        expected_yield=Quotation(units=0, nano=-350000000),
        positions=list(portfolio_positions.values()),
    )


@pytest.fixture()
def mock_operations_service(
    real_services: Services,
    mocker,
    portfolio_response: PortfolioResponse,
) -> Services:
    real_services.operations = mocker.Mock(wraps=real_services.operations)
    real_services.operations.get_portfolio.return_value = portfolio_response

    return real_services


@pytest.fixture()
def mock_users_service(
    real_services: Services,
    mocker,
    marginal_trade_active: bool,
) -> Services:
    real_services.users = mocker.Mock(wraps=real_services.users)
    if marginal_trade_active:
        real_services.users.get_margin_attributes.return_value = (
            GetMarginAttributesResponse(
                liquid_portfolio=MoneyValue(currency="", units=0, nano=0),
                starting_margin=MoneyValue(currency="", units=0, nano=0),
                minimal_margin=MoneyValue(currency="", units=0, nano=0),
                funds_sufficiency_level=Quotation(units=322, nano=0),
                amount_of_missing_funds=MoneyValue(currency="", units=0, nano=0),
            )
        )
    else:
        real_services.users.get_margin_attributes.side_effect = RequestError(
            code=StatusCode.PERMISSION_DENIED,
            details="Marginal trade disabled",
            metadata=None,
        )

    return real_services


@pytest.fixture()
def marginal_trade_active() -> bool:
    return True


@pytest.fixture()
def mock_orders_service(
    real_services: Services,
    mocker,
    portfolio_positions: Dict[str, PortfolioPosition],
    balance: MoneyValue,
    current_market_data: List[Candle],
    settings: MovingAverageStrategySettings,
    marginal_trade_active: bool,
) -> Services:
    real_services.orders = mocker.Mock(wraps=real_services.orders)

    def _post_order(
        *,
        figi: str = "",
        quantity: int = 0,
        price: Optional[Quotation] = None,
        direction: OrderDirection = OrderDirection(0),
        account_id: str = "",
        order_type: OrderType = OrderType(0),
        order_id: str = "",
    ):
        assert figi == settings.share_id
        assert quantity > 0
        assert account_id == settings.account_id
        assert order_type.ORDER_TYPE_MARKET

        last_candle = current_market_data[-1]
        last_market_price = quotation_to_decimal(last_candle.close)

        position = portfolio_positions.get(figi)
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
            Quotation(units=balance.units, nano=balance.nano)
        )
        new_balance = decimal_to_quotation(old_balance + balance_delta)

        if quotation_to_decimal(new_balance) < 0:
            logger.warning(
                "You have debt!, Balance: %s", quotation_to_decimal(new_balance)
            )
            raise RequestError(
                code=StatusCode.ABORTED,
                details=f"Not enough money: {old_balance}",
                metadata=None,
            )

        balance.units = new_balance.units
        balance.nano = new_balance.nano

        portfolio_positions[figi] = position

    real_services.orders.post_order = _post_order

    return real_services


@pytest.fixture()
def mocked_services(
    real_services: Services,
    mock_market_data_service,
    mock_market_data_stream_service,
    mock_operations_service,
    mock_users_service,
    mock_orders_service,
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
        candle_interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        long_period=timedelta(minutes=100),
        short_period=timedelta(minutes=20),
        std_period=timedelta(minutes=30),
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
    state: MovingAverageStrategyState,
    settings: MovingAverageStrategySettings,
) -> MovingAverageSignalExecutor:
    return MovingAverageSignalExecutor(
        services=mocked_services,
        state=state,
        settings=settings,
    )


@pytest.fixture()
def supervisor(
) -> MovingAverageStrategySupervisor:
    return MovingAverageStrategySupervisor(
    )


@pytest.fixture()
def moving_average_strategy_trader(
    strategy: MovingAverageStrategy,
    settings: MovingAverageStrategySettings,
    mocked_services: Services,
    state: MovingAverageStrategyState,
    signal_executor: MovingAverageSignalExecutor,
    account_manager: AccountManager,
    supervisor: MovingAverageStrategySupervisor,
) -> MovingAverageStrategyTrader:
    return MovingAverageStrategyTrader(
        strategy=strategy,
        settings=settings,
        services=mocked_services,
        state=state,
        signal_executor=signal_executor,
        account_manager=account_manager,
        supervisor=supervisor,
    )


@pytest.fixture()
def plotter(
    settings: MovingAverageStrategySettings,
) -> MovingAverageStrategyPlotter:
    return MovingAverageStrategyPlotter(settings=settings    )


class TestMovingAverageStrategyTrader:
    @pytest.mark.freeze_time()
    def test_trade(
        self,
        moving_average_strategy_trader: MovingAverageStrategyTrader,
        strategy: MovingAverageStrategy,
        account_manager: AccountManager,
        signal_executor: MovingAverageSignalExecutor,
        plotter: MovingAverageStrategyPlotter,
        supervisor: MovingAverageStrategySupervisor,
        caplog,
        freezer,
    ):
        caplog.set_level(logging.DEBUG)
        caplog.set_level(logging.INFO)

        initial_balance = account_manager.get_current_balance()

        for i in range(5):
            logger.info("Trade %s", i)
            moving_average_strategy_trader.trade()

        current_balance = account_manager.get_current_balance()
        assert initial_balance != current_balance
        logger.info("Initial balance %s", initial_balance)
        logger.info("Current balance %s", current_balance)

        events = supervisor.get_events()
        plotter.plot(events)
