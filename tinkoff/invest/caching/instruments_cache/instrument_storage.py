import logging
from dataclasses import replace
from typing import Generic

from tinkoff.invest import InstrumentIdType
from tinkoff.invest.caching.instruments_cache.models import TInstrumentResponse, \
    TInstrumentsResponse

logger = logging.getLogger(__name__)


class InstrumentStorage(Generic[TInstrumentResponse, TInstrumentsResponse]):
    def __init__(self, instruments_response: TInstrumentsResponse):
        self._instruments_response = instruments_response

        self._instrument_by_class_code_figi = {(instrument.class_code, instrument.figi): instrument for instrument in self._instruments_response.instruments}
        self._instrument_by_class_code_ticker = {(instrument.class_code, instrument.ticker): instrument for instrument in self._instruments_response.instruments}
        self._instrument_by_class_code_uid = {(instrument.class_code, instrument.uid): instrument for instrument in self._instruments_response.instruments}

        self._instrument_by_class_code_id_index = {
            InstrumentIdType.INSTRUMENT_ID_UNSPECIFIED: self._instrument_by_class_code_figi,
            InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI: self._instrument_by_class_code_figi,
            InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER: self._instrument_by_class_code_ticker,
            InstrumentIdType.INSTRUMENT_ID_TYPE_UID: self._instrument_by_class_code_uid,
        }

    def get(self, *, id_type: InstrumentIdType, class_code: str, id: str) -> TInstrumentResponse:
        logger.debug(f'Cache request id_type=%s, class_code=%s, id=%s', id_type, class_code, id)
        instrument_by_class_code_id = self._instrument_by_class_code_id_index[id_type]
        logger.debug(f'Index for %s found: \n%s', id_type, instrument_by_class_code_id.keys())
        key = (class_code, id)
        logger.debug(f'Cache request key=%s', key)

        return instrument_by_class_code_id[key]

    def get_instruments_response(self) -> TInstrumentsResponse:
        return replace(self._instruments_response, **{})
