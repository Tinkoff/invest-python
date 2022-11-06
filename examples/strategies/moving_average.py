import logging
import os
from datetime import timedelta
from decimal import Decimal

from matplotlib import pyplot as plt

from tinkoff.invest import CandleInterval, Client
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
from tinkoff.invest.strategies.moving_average.strategy_state import (
    MovingAverageStrategyState,
)
from tinkoff.invest.strategies.moving_average.supervisor import (
    MovingAverageStrategySupervisor,
)
from tinkoff.invest.strategies.moving_average.trader import MovingAverageStrategyTrader

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN = os.environ["INVEST_TOKEN"]
FIGI = os.environ["INVEST_FIGI"]
ACCOUNT_ID = os.environ["INVEST_ACCOUNT_ID"]


def main():
    with Client(TOKEN) as services:
        settings = MovingAverageStrategySettings(
            share_id=FIGI,
            account_id=ACCOUNT_ID,
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
        supervisor = MovingAverageStrategySupervisor()
        trader = MovingAverageStrategyTrader(
            strategy=strategy,
            settings=settings,
            services=services,
            state=state,
            signal_executor=signal_executor,
            account_manager=account_manager,
            supervisor=supervisor,
        )
        plotter = MovingAverageStrategyPlotter(settings=settings)

        initial_balance = account_manager.get_current_balance()

        for i in range(5):
            logger.info("Trade %s", i)
            trader.trade()

        current_balance = account_manager.get_current_balance()

        logger.info("Initial balance %s", initial_balance)
        logger.info("Current balance %s", current_balance)

        events = supervisor.get_events()
        plotter.plot(events)
        plt.show()
