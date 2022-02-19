from dataclasses import dataclass
from datetime import datetime

from tinkoff.invest.strategies.base.models import CandleEvent
from tinkoff.invest.strategies.base.signal import Signal


@dataclass
class StrategyEvent:
    time: datetime


@dataclass
class DataEvent(StrategyEvent):
    candle_event: CandleEvent


@dataclass
class SignalEvent(StrategyEvent):
    signal: Signal
    was_executed: bool
