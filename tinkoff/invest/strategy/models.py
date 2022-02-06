from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(eq=False, repr=True)
class Candle:
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


@dataclass(eq=False, repr=True)
class CandleEvent:
    candle: Candle
    volume: int
    time: datetime
    is_complete: bool
