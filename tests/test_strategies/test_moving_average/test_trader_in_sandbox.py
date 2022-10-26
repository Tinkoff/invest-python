import logging
import os
from datetime import timedelta
from decimal import Decimal
from typing import Iterator

import pytest

from tinkoff.invest import (
    CandleInterval,
    Client,
    GetMarginAttributesResponse,
    InstrumentIdType,
    MoneyValue,
    OpenSandboxAccountResponse,
    Quotation,
    ShareResponse,
    TradingSchedulesResponse,
)
from tinkoff.invest.services import SandboxService, Services
from tinkoff.invest.strategies.base.account_manager import AccountManager
from tinkoff.invest.strategies.base.errors import MarketDataNotAvailableError
from tinkoff.invest.strategies.moving_average.plotter import (
    MovingAverageStrategyPlotter,
)
from tinkoff.invest.strategies.moving_average.signal_executor import (
    MovingAverageSignalExecutor,
)
from tinkoff.invest.strategies.moving_average.strategy import MovingAverageStrategy
from tinkoff.invest.strategies.moving_average.strategy_settings import (
    MovingAverageStrategySettings,
)
from tinkoff.invest.strategies.moving_average.supervisor import (
    MovingAverageStrategySupervisor,
)
from tinkoff.invest.strategies.moving_average.trader import MovingAverageStrategyTrader
from tinkoff.invest.typedefs import AccountId, ShareId
from tinkoff.invest.utils import now

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture()
def token() -> str:
    return os.environ["INVEST_SANDBOX_TOKEN"]


@pytest.fixture()
def account(
    token: str, real_services: Services, balance: MoneyValue
) -> Iterator[OpenSandboxAccountResponse]:
    sandbox: SandboxService = real_services.sandbox
    account_response = sandbox.open_sandbox_account()
    account_id = account_response.account_id
    sandbox.sandbox_pay_in(account_id=account_id, amount=balance)

    yield account_response

    sandbox.close_sandbox_account(account_id=account_id)


@pytest.fixture()
def account_id(account: OpenSandboxAccountResponse) -> str:
    return account.account_id


@pytest.fixture()
def mock_market_data_service(real_services: Services) -> Services:
    return real_services


@pytest.fixture()
def mock_market_data_stream_service(real_services: Services) -> Services:
    return real_services


@pytest.fixture()
def mock_operations_service(real_services: Services) -> Services:
    real_services.operations.get_portfolio = real_services.sandbox.get_sandbox_portfolio
    real_services.operations.get_operations = (
        real_services.sandbox.get_sandbox_operations
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
def mock_orders_service(real_services: Services) -> Services:
    real_services.orders.post_order = real_services.sandbox.post_sandbox_order
    real_services.orders.get_orders = real_services.sandbox.get_sandbox_orders
    real_services.orders.cancel_order = real_services.sandbox.cancel_sandbox_order
    real_services.orders.get_order_state = real_services.sandbox.get_sandbox_order_state
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
def figi() -> str:
    return "BBG004730N88"


@pytest.fixture()
def balance() -> MoneyValue:
    return MoneyValue(currency="rub", units=20050, nano=690000000)


@pytest.fixture()
def settings(figi: str, account_id: AccountId) -> MovingAverageStrategySettings:
    return MovingAverageStrategySettings(
        share_id=ShareId(figi),
        account_id=account_id,
        max_transaction_price=Decimal(10000),
        candle_interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        long_period=timedelta(hours=200),
        short_period=timedelta(hours=50),
        std_period=timedelta(hours=30),
    )


@pytest.fixture(autouse=True)
def _ensure_is_market_active(
    settings: MovingAverageStrategySettings,
):
    token = os.environ.get("INVEST_SANDBOX_TOKEN")
    if token is None:
        pytest.skip("INVEST_SANDBOX_TOKEN should be specified")

    with Client(token) as client:
        share_response: ShareResponse = client.instruments.share_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=settings.share_id
        )
        logger.debug("Instrument = %s", share_response.instrument.name)
        response: TradingSchedulesResponse = client.instruments.trading_schedules(
            exchange=share_response.instrument.exchange,
            from_=now(),
            to=now(),
        )
        (exchange,) = response.exchanges
        logger.debug("Exchange = %s", exchange.exchange)
        (day,) = exchange.days
        if day.is_trading_day and day.start_time < now() < day.end_time:
            return

    pytest.skip("test skipped because market is closed")


@pytest.mark.skipif(
    os.environ.get("INVEST_SANDBOX_TOKEN") is None,
    reason="INVEST_SANDBOX_TOKEN should be specified",
)
class TestMovingAverageStrategyTraderInSandbox:
    def test_trade(
        self,
        moving_average_strategy_trader: MovingAverageStrategyTrader,
        strategy: MovingAverageStrategy,
        account_manager: AccountManager,
        signal_executor: MovingAverageSignalExecutor,
        plotter: MovingAverageStrategyPlotter,
        supervisor: MovingAverageStrategySupervisor,
        caplog,
    ):
        caplog.set_level(logging.DEBUG)
        caplog.set_level(logging.INFO)

        initial_balance = account_manager.get_current_balance()

        try:
            for i in range(50):
                logger.info("Trade %s", i)
                moving_average_strategy_trader.trade()
        except MarketDataNotAvailableError:
            pass

        events = supervisor.get_events()
        plotter.plot(events)

        current_balance = account_manager.get_current_balance()
        assert initial_balance != current_balance
        logger.info("Initial balance %s", initial_balance)
        logger.info("Current balance %s", current_balance)
