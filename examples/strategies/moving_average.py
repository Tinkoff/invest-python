import logging
from datetime import timedelta
from decimal import Decimal

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.strategies.base.account_manager import AccountManager
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
from tinkoff.invest.strategies.moving_average.trader import MovingAverageStrategyTrader
from tinkoff.invest.env_tools.token import TOKEN
from tinkoff.invest.typedefs import AccountId, ShareId

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    with Client(TOKEN) as services:
        figi = "BBG0047315Y7"
        account_id = AccountId("1337007228")
        settings = MovingAverageStrategySettings(
            share_id=ShareId(figi),
            account_id=account_id,
            max_transaction_price=Decimal(10000),
            candle_interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
            long_period=timedelta(minutes=100),
            short_period=timedelta(minutes=20),
            std_period=timedelta(minutes=30),
        )

        account_manager = AccountManager(services=services, strategy_settings=settings)
        state = MovingAverageStrategyState()
        strategy = MovingAverageStrategy(
            settings=settings,
            account_manager=account_manager,
            state=state,
        )
        signal_executor = MovingAverageSignalExecutor(
            services=services,
            state=state,
            settings=settings,
        )
        trader = MovingAverageStrategyTrader(
            strategy=strategy,
            settings=settings,
            services=services,
            state=state,
            signal_executor=signal_executor,
            account_manager=account_manager,
        )

        initial_balance = account_manager.get_current_balance()

        for i in range(5):
            logger.info("Trade %s", i)
            trader.trade()

        current_balance = account_manager.get_current_balance()

        logger.info("Initial balance %s", initial_balance)
        logger.info("Current balance %s", current_balance)
        strategy.plot()
