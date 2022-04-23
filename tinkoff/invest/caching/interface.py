import abc
from datetime import datetime
from typing import Tuple, Generic, TypeVar, Iterable

from tinkoff.invest.caching.instrument_market_data_storage import \
    InstrumentDateRangeData

TInstrumentData = TypeVar('TInstrumentData')


class IInstrumentMarketDataStorage(abc.ABC, Generic[TInstrumentData]):
    def get(self, request_range: Tuple[datetime, datetime]) -> Iterable[InstrumentDateRangeData]:
        pass

    def update(self, data_list: Iterable[InstrumentDateRangeData]):
        pass
