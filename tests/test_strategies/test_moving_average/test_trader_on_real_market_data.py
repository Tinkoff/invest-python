import logging
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Dict, Iterable, List

import pytest

from tinkoff.invest import (
    Candle,
    CandleInterval,
    HistoricCandle,
    MarketDataResponse,
    MoneyValue,
    PortfolioPosition,
    PortfolioResponse,
    Quotation,
)
from tinkoff.invest.services import Services
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
from tinkoff.invest.utils import candle_interval_to_subscription_interval, now

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture()
def token() -> str:
    return os.environ["INVEST_TOKEN"]


@pytest.fixture()
def real_market_data_test_from(request) -> datetime:
    return request.param


@pytest.fixture()
def real_market_data_test_start(request) -> datetime:
    return request.param


@pytest.fixture()
def real_market_data_test_end(request) -> datetime:
    return request.param


@pytest.fixture()
def real_market_data(
    real_services: Services,
    real_market_data_test_from: datetime,
    real_market_data_test_end: datetime,
    figi: str,
    settings: MovingAverageStrategySettings,
) -> Iterable[HistoricCandle]:
    candles = []
    for candle in real_services.get_all_candles(
        figi=figi,
        from_=real_market_data_test_from,
        to=real_market_data_test_end,
        interval=settings.candle_interval,
    ):
        candles.append(candle)
    return candles


@pytest.fixture()
def initial_candles(
    real_market_data_test_start: datetime,
    real_market_data: Iterable[HistoricCandle],
) -> Iterable[HistoricCandle]:
    return [
        candle
        for candle in real_market_data
        if candle.time < real_market_data_test_start
    ]


@pytest.fixture()
def after_start_candles(
    real_market_data_test_start: datetime,
    real_market_data: Iterable[HistoricCandle],
) -> Iterable[HistoricCandle]:
    return [
        candle
        for candle in real_market_data
        if candle.time >= real_market_data_test_start
    ]


@pytest.fixture()
def current_market_data() -> List[Candle]:
    return []


@pytest.fixture()
def mock_market_data_stream_service(
    real_services: Services,
    mocker,
    figi: str,
    settings: MovingAverageStrategySettings,
    current_market_data: List[Candle],
    freezer,
    after_start_candles: Iterable[HistoricCandle],
    real_market_data_test_from: datetime,
    real_market_data_test_start: datetime,
    real_market_data_test_end: datetime,
) -> Services:
    real_services.market_data_stream = mocker.Mock(
        wraps=real_services.market_data_stream
    )
    freezer.move_to(real_market_data_test_start)

    def _market_data_stream(*args, **kwargs):
        yield MarketDataResponse(candle=None)  # type: ignore

        interval = candle_interval_to_subscription_interval(settings.candle_interval)
        for historic_candle in after_start_candles:
            candle = Candle(
                figi=figi,
                interval=interval,
                open=historic_candle.open,
                high=historic_candle.high,
                low=historic_candle.low,
                close=historic_candle.close,
                volume=historic_candle.volume,
                time=historic_candle.time,
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
        short_period=timedelta(minutes=50),
        std_period=timedelta(minutes=30),
    )


def start_datetime() -> datetime:
    return datetime(year=2022, month=2, day=16, hour=17, tzinfo=timezone.utc)


class TestMovingAverageStrategyTraderRealMarketData:
    @pytest.mark.skipif(
        os.environ.get("INVEST_TOKEN") is None,
        reason="Run locally with token specified",
    )
    @pytest.mark.freeze_time()
    @pytest.mark.parametrize(
        (
            "real_market_data_test_from",
            "real_market_data_test_start",
            "real_market_data_test_end",
        ),
        [
            (
                start_datetime() - timedelta(days=1),
                start_datetime(),
                start_datetime() + timedelta(days=3),
            )
        ],
        indirect=True,
    )
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

        for i in range(50):
            logger.info("Trade %s", i)
            moving_average_strategy_trader.trade()

        events = supervisor.get_events()
        plotter.plot(events)

        current_balance = account_manager.get_current_balance()
        assert initial_balance != current_balance
        logger.info("Initial balance %s", initial_balance)
        logger.info("Current balance %s", current_balance)
