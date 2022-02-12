import dataclasses
from datetime import timedelta

from tinkoff.invest.strategies.base.strategy_settings_base import StrategySettings


@dataclasses.dataclass
class MovingAverageStrategySettings(StrategySettings):
    long_period: timedelta
    short_period: timedelta
    std_period: timedelta
