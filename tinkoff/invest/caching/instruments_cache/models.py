from typing import List, TypeVar


class InstrumentResponse:
    class_code: str

    figi: str
    ticker: str
    uid: str


class InstrumentsResponse:
    instruments: List[InstrumentResponse]


TInstrumentResponse = TypeVar("TInstrumentResponse", bound=InstrumentResponse)
TInstrumentsResponse = TypeVar("TInstrumentsResponse", bound=InstrumentsResponse)
