import abc
from datetime import datetime
from typing import Generic, Iterable, Tuple, TypeVar

from tinkoff.invest.caching.instrument_date_range_market_data import (
    InstrumentDateRangeData,
)

TInstrumentData = TypeVar("TInstrumentData")


class IInstrumentMarketDataStorage(abc.ABC, Generic[TInstrumentData]):
    def get(
        self, request_range: Tuple[datetime, datetime]
    ) -> Iterable[InstrumentDateRangeData]:
        pass

    def update(self, data_list: Iterable[InstrumentDateRangeData]):
        pass
