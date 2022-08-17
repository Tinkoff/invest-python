from typing import List


class InstrumentResponse:
    class_code: str

    figi: str
    ticker: str
    uid: str


class InstrumentsResponse:
    instruments: List[InstrumentResponse]
