import logging
import uuid
from pprint import pprint
from typing import Iterator, List, Dict, Type

import pytest

from tinkoff.invest import Client, InstrumentIdType, EtfsResponse, Etf, SharesResponse, \
    Share, BondsResponse, Bond, CurrenciesResponse, Currency, FuturesResponse, Future, \
    InstrumentResponse, EtfResponse, ShareResponse, BondResponse, CurrencyResponse, \
    FutureResponse
from tinkoff.invest.caching.instruments_cache.instruments_cache import InstrumentsCache
from tinkoff.invest.caching.instruments_cache.models import InstrumentsResponse
from tinkoff.invest.caching.instruments_cache.settings import InstrumentsCacheSettings
from tinkoff.invest.services import Services, InstrumentsService


def uid() -> str:
    return uuid.uuid4().hex


@pytest.fixture()
def token() -> str:
    return uid()


@pytest.fixture()
def real_services(token: str) -> Iterator[Services]:
    with Client(token) as services:
        yield services


def gen_meta_ids() -> Dict[str, str]:
    return dict(class_code=uid(), figi=uid(), ticker=uid(), uid=uid())


def gen_instruments(type_: Type, instrument_count: int = 10):
    return [type_(name=f'{type_.__name__}_{i}', **gen_meta_ids()) for i in
            range(instrument_count)]


def gen_instruments_response(response_type: Type, type_: Type,
                             instrument_count: int = 10):
    return response_type(instruments=gen_instruments(type_, instrument_count))


@pytest.fixture()
def instrument_map():
    return {
        Etf: gen_instruments_response(EtfsResponse, Etf),
        Share: gen_instruments_response(SharesResponse, Share),
        Bond: gen_instruments_response(BondsResponse, Bond),
        Currency: gen_instruments_response(CurrenciesResponse, Currency),
        Future: gen_instruments_response(FuturesResponse, Future),
    }


def mock_get_by(instrument_response: InstrumentsResponse, response_type):
    type_to_field_extractor = {
        InstrumentIdType.INSTRUMENT_ID_UNSPECIFIED: lambda i: i.figi,
        InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI: lambda i: i.figi,
        InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER: lambda i: i.ticker,
        InstrumentIdType.INSTRUMENT_ID_TYPE_UID: lambda i: i.uid,
    }

    def _mock_get_by(
            *,
            id_type: InstrumentIdType = InstrumentIdType(0),
            class_code: str = "",
            id: str = "",
    ):
        get_id = type_to_field_extractor[id_type]

        def filter_(instrument):
            return get_id(instrument) == id and instrument.class_code == class_code

        found_instrument, = filter(filter_, instrument_response.instruments)
        return response_type(instrument=found_instrument)

    return _mock_get_by


@pytest.fixture()
def mock_instruments_service(
        real_services: Services,
        mocker,
        instrument_map,
) -> Services:
    real_services.instruments: InstrumentsService = mocker.Mock(
        wraps=real_services.instruments,
    )

    real_services.instruments.etfs.__name__ = 'etfs'
    real_services.instruments.etfs.return_value = instrument_map[Etf]
    real_services.instruments.etf_by = mock_get_by(instrument_map[Etf], EtfResponse)

    real_services.instruments.shares.__name__ = 'shares'
    real_services.instruments.shares.return_value = instrument_map[Share]
    real_services.instruments.share_by = mock_get_by(instrument_map[Share], ShareResponse)

    real_services.instruments.bonds.__name__ = 'bonds'
    real_services.instruments.bonds.return_value = instrument_map[Bond]
    real_services.instruments.bond_by = mock_get_by(instrument_map[Bond], BondResponse)

    real_services.instruments.currencies.__name__ = 'currencies'
    real_services.instruments.currencies.return_value = instrument_map[Currency]
    real_services.instruments.currency_by = mock_get_by(instrument_map[Currency], CurrencyResponse)

    real_services.instruments.futures.__name__ = 'futures'
    real_services.instruments.futures.return_value = instrument_map[Future]
    real_services.instruments.future_by = mock_get_by(instrument_map[Future], FutureResponse)

    return real_services


@pytest.fixture()
def mocked_services(
        real_services: Services,
        mock_instruments_service,
) -> Services:
    return real_services


class TestInstrumentCache:
    def test_a(self, mocked_services: Services, ):
        inst = mocked_services.instruments.etfs().instruments[0]

        from_server = mocked_services.instruments.etf_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
            class_code=inst.class_code,
            id=inst.uid,
        )
        pprint(from_server)

        settings = InstrumentsCacheSettings()
        instruments_cache = InstrumentsCache(
            settings=settings, instruments_service=mocked_services.instruments
        )

        from_cache = instruments_cache.etf_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
            class_code=inst.class_code,
            id=inst.uid,
        )
        pprint(from_cache)

        assert str(from_server) == str(from_cache)
