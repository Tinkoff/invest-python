from typing import Protocol

from tinkoff.invest import InstrumentStatus

from .models import InstrumentsResponse


class InstrumentsResponseCallable(Protocol):
    def __call__(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> InstrumentsResponse:
        ...

    def __name__(self) -> str:
        ...
