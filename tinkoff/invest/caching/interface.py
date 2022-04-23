import abc
from datetime import datetime
from typing import Tuple, Generic, TypeVar


TInstrumentData = TypeVar('TInstrumentData')


class IInstrumentMarketDataStorage(abc.ABC, Generic[TInstrumentData]):
    def __getitem__(self, date_range: Tuple[datetime, datetime]):
        pass

    def __setitem__(self, date_range: Tuple[datetime, datetime], data: TInstrumentData):
        pass
