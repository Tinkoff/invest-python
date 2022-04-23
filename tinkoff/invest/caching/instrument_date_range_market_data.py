import dataclasses
from datetime import datetime
from typing import Tuple, Iterable

from tinkoff.invest.schemas import HistoricCandle


@dataclasses.dataclass()
class InstrumentDateRangeData:
    date_range: Tuple[datetime, datetime]
    historic_candles: Iterable[HistoricCandle]