from typing import Protocol

from tinkoff.invest import InstrumentStatus
from tinkoff.invest.caching.instruments_cache.models import InstrumentsResponse


class InstrumentsResponseCallable(Protocol):
    def __call__(self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)) -> InstrumentsResponse:
        ...
