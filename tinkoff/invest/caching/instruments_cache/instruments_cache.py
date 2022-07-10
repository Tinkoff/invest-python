import logging
from typing import cast

from cachetools import TTLCache

from tinkoff.invest import (
    Bond,
    BondResponse,
    BondsResponse,
    CurrenciesResponse,
    Currency,
    CurrencyResponse,
    Etf,
    EtfResponse,
    EtfsResponse,
    Future,
    FutureResponse,
    FuturesResponse,
    InstrumentIdType,
    InstrumentStatus,
    Share,
    ShareResponse,
    SharesResponse,
)
from tinkoff.invest.caching.instruments_cache.instrument_storage import (
    InstrumentStorage,
)
from tinkoff.invest.caching.instruments_cache.interface import IInstrumentsGetter
from tinkoff.invest.caching.instruments_cache.models import (
    InstrumentResponse,
    InstrumentsResponse,
)
from tinkoff.invest.caching.instruments_cache.protocol import (
    InstrumentsResponseCallable,
)
from tinkoff.invest.caching.instruments_cache.settings import InstrumentsCacheSettings
from tinkoff.invest.services import InstrumentsService

logger = logging.getLogger(__name__)


class InstrumentsCache(IInstrumentsGetter):
    def __init__(
        self,
        settings: InstrumentsCacheSettings,
        instruments_service: InstrumentsService,
    ):
        self._settings = settings
        self._instruments_service = instruments_service

        logger.debug("Initialising instruments cache")
        self._instruments_methods = [
            self.shares,
            self.futures,
            self.etfs,
            self.bonds,
            self.currencies,
        ]
        self._cache = TTLCache(
            maxsize=len(self._instruments_methods),
            ttl=self._settings.ttl.total_seconds(),
        )
        self._refresh_cache()

    def _refresh_cache(self):
        logger.debug("Refreshing instruments cache")
        for instruments_method in self._instruments_methods:
            instruments_method()
        self._assert_cache()

    def _assert_cache(self):
        assert self._cache.keys() == set(
            map(lambda f: f.__name__, self._instruments_methods)
        ), f"Cache does not have all instrument types {self._cache}"

    def _get_instrument_storage(
        self, get_instruments_method: InstrumentsResponseCallable
    ) -> InstrumentStorage[InstrumentResponse, InstrumentsResponse]:
        storage_key = get_instruments_method.__name__
        storage = self._cache.get(storage_key)
        if storage is not None:
            logger.debug("Got storage for key %s from cache", storage_key)
            return storage
        logger.debug(
            "Storage for key %s not found, creating new storage with ttl=%s",
            storage_key,
            self._cache.ttl,
        )
        instruments_response = get_instruments_method(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL
        )
        storage = InstrumentStorage(instruments_response=instruments_response)
        self._cache[storage_key] = storage
        return storage  # noqa: R504

    def shares(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> SharesResponse:
        storage = cast(
            InstrumentStorage[ShareResponse, SharesResponse],
            self._get_instrument_storage(self._instruments_service.shares),
        )
        return storage.get_instruments_response()

    def share_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> ShareResponse:
        storage = cast(
            InstrumentStorage[Share, SharesResponse],
            self._get_instrument_storage(self._instruments_service.shares),
        )
        share = storage.get(id_type=id_type, class_code=class_code, id=id)
        return ShareResponse(instrument=share)

    def futures(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> FuturesResponse:
        storage = cast(
            InstrumentStorage[FutureResponse, FuturesResponse],
            self._get_instrument_storage(self._instruments_service.futures),
        )
        return storage.get_instruments_response()

    def future_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> FutureResponse:
        storage = cast(
            InstrumentStorage[Future, FuturesResponse],
            self._get_instrument_storage(self._instruments_service.futures),
        )
        future = storage.get(id_type=id_type, class_code=class_code, id=id)
        return FutureResponse(instrument=future)

    def etfs(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> EtfsResponse:
        storage = cast(
            InstrumentStorage[EtfResponse, EtfsResponse],
            self._get_instrument_storage(self._instruments_service.etfs),
        )
        return storage.get_instruments_response()

    def etf_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> EtfResponse:
        storage = cast(
            InstrumentStorage[Etf, EtfsResponse],
            self._get_instrument_storage(self._instruments_service.etfs),
        )
        etf = storage.get(id_type=id_type, class_code=class_code, id=id)
        return EtfResponse(instrument=etf)

    def bonds(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> BondsResponse:
        storage = cast(
            InstrumentStorage[BondResponse, BondsResponse],
            self._get_instrument_storage(self._instruments_service.bonds),
        )
        return storage.get_instruments_response()

    def bond_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> BondResponse:
        storage = cast(
            InstrumentStorage[Bond, BondsResponse],
            self._get_instrument_storage(self._instruments_service.bonds),
        )
        bond = storage.get(id_type=id_type, class_code=class_code, id=id)
        return BondResponse(instrument=bond)

    def currencies(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> CurrenciesResponse:
        storage = cast(
            InstrumentStorage[CurrencyResponse, CurrenciesResponse],
            self._get_instrument_storage(self._instruments_service.currencies),
        )
        return storage.get_instruments_response()

    def currency_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> CurrencyResponse:
        storage = cast(
            InstrumentStorage[Currency, CurrenciesResponse],
            self._get_instrument_storage(self._instruments_service.currencies),
        )
        currency = storage.get(id_type=id_type, class_code=class_code, id=id)
        return CurrencyResponse(instrument=currency)
