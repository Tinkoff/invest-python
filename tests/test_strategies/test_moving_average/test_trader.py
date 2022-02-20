import logging
from datetime import timedelta
from decimal import Decimal
from typing import Dict

import pytest

from tinkoff.invest import (
    CandleInterval,
    MoneyValue,
    PortfolioPosition,
    PortfolioResponse,
    Quotation,
)
from tinkoff.invest.strategies.base.account_manager import AccountManager
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

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture()
def token() -> str:
    return "some"


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
