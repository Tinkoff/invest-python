import random
import time
import uuid
from datetime import timedelta
from typing import Any, Callable, Dict, Iterator, Type
from unittest.mock import Mock

import pytest

from tinkoff.invest import (
    Bond,
    BondResponse,
    BondsResponse,
    Client,
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
    InstrumentResponse,
    Share,
    ShareResponse,
    SharesResponse,
)
from tinkoff.invest.caching.instruments_cache.instruments_cache import InstrumentsCache
from tinkoff.invest.caching.instruments_cache.models import InstrumentsResponse
from tinkoff.invest.caching.instruments_cache.settings import InstrumentsCacheSettings
from tinkoff.invest.services import InstrumentsService, Services


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
    return {"class_code": uid(), "figi": uid(), "ticker": uid(), "uid": uid()}


def gen_instruments(type_: Type, instrument_count: int = 10):
    return [
        type_(name=f"{type_.__name__}_{i}", **gen_meta_ids())
        for i in range(instrument_count)
    ]


def gen_instruments_response(
    response_type: Type, type_: Type, instrument_count: int = 10
):
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

        (found_instrument,) = filter(filter_, instrument_response.instruments)
        return response_type(instrument=found_instrument)

    return Mock(wraps=_mock_get_by)


@pytest.fixture()
def mock_instruments_service(
    real_services: Services,
    mocker,
    instrument_map,
) -> Services:
    real_services.instruments: InstrumentsService = mocker.Mock(
        wraps=real_services.instruments,
    )

    real_services.instruments.etfs.__name__ = "etfs"
    real_services.instruments.etfs.return_value = instrument_map[Etf]
    real_services.instruments.etf_by = mock_get_by(instrument_map[Etf], EtfResponse)

    real_services.instruments.shares.__name__ = "shares"
    real_services.instruments.shares.return_value = instrument_map[Share]
    real_services.instruments.share_by = mock_get_by(
        instrument_map[Share], ShareResponse
    )

    real_services.instruments.bonds.__name__ = "bonds"
    real_services.instruments.bonds.return_value = instrument_map[Bond]
    real_services.instruments.bond_by = mock_get_by(instrument_map[Bond], BondResponse)

    real_services.instruments.currencies.__name__ = "currencies"
    real_services.instruments.currencies.return_value = instrument_map[Currency]
    real_services.instruments.currency_by = mock_get_by(
        instrument_map[Currency], CurrencyResponse
    )

    real_services.instruments.futures.__name__ = "futures"
    real_services.instruments.futures.return_value = instrument_map[Future]
    real_services.instruments.future_by = mock_get_by(
        instrument_map[Future], FutureResponse
    )

    return real_services


@pytest.fixture()
def mocked_services(
    real_services: Services,
    mock_instruments_service,
) -> Services:
    return real_services


@pytest.fixture()
def settings() -> InstrumentsCacheSettings:
    return InstrumentsCacheSettings()


@pytest.fixture()
def instruments_cache(
    settings: InstrumentsCacheSettings, mocked_services
) -> InstrumentsCache:
    return InstrumentsCache(
        settings=settings, instruments_service=mocked_services.instruments
    )


@pytest.mark.parametrize(
    ("get_instruments_of_type", "get_instrument_of_type_by"),
    [
        (
            lambda instruments: instruments.etfs,
            lambda instruments: instruments.etf_by,
        ),
        (
            lambda instruments: instruments.shares,
            lambda instruments: instruments.share_by,
        ),
        (
            lambda instruments: instruments.bonds,
            lambda instruments: instruments.bond_by,
        ),
        (
            lambda instruments: instruments.currencies,
            lambda instruments: instruments.currency_by,
        ),
        (
            lambda instruments: instruments.futures,
            lambda instruments: instruments.future_by,
        ),
    ],
)
@pytest.mark.parametrize(
    ("id_type", "get_id"),
    [
        (
            InstrumentIdType.INSTRUMENT_ID_UNSPECIFIED,
            lambda instrument: instrument.figi,
        ),
        (
            InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            lambda instrument: instrument.figi,
        ),
        (
            InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
            lambda instrument: instrument.ticker,
        ),
        (
            InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
            lambda instrument: instrument.uid,
        ),
    ],
)
class TestInstrumentCache:
    def test_gets_from_net_then_cache(
        self,
        mocked_services: Services,
        settings: InstrumentsCacheSettings,
        instruments_cache: InstrumentsCache,
        get_instruments_of_type: Callable[
            [InstrumentsService], Callable[[], InstrumentsResponse]
        ],
        get_instrument_of_type_by: Callable[
            [InstrumentsService],
            Callable[[InstrumentIdType, str, str], InstrumentResponse],
        ],
        id_type: InstrumentIdType,
        get_id: Callable[[Any], str],
    ):
        get_instruments = get_instruments_of_type(mocked_services.instruments)
        get_instrument_by = get_instrument_of_type_by(mocked_services.instruments)
        get_instrument_by_cached = get_instrument_of_type_by(instruments_cache)
        (inst,) = random.sample(get_instruments().instruments, k=1)
        from_server = get_instrument_by(
            id_type=id_type,
            class_code=inst.class_code,
            id=get_id(inst),
        )
        get_instrument_by.assert_called_once()
        get_instrument_by.reset_mock()

        from_cache = get_instrument_by_cached(
            id_type=id_type,
            class_code=inst.class_code,
            id=get_id(inst),
        )

        get_instrument_by.assert_not_called()
        assert str(from_server) == str(from_cache)

    @pytest.mark.parametrize(
        "settings", [InstrumentsCacheSettings(ttl=timedelta(milliseconds=10))]
    )
    def test_refreshes_on_ttl(
        self,
        mocked_services: Services,
        settings: InstrumentsCacheSettings,
        instruments_cache: InstrumentsCache,
        get_instruments_of_type: Callable[
            [InstrumentsService], Callable[[], InstrumentsResponse]
        ],
        get_instrument_of_type_by: Callable[
            [InstrumentsService],
            Callable[[InstrumentIdType, str, str], InstrumentResponse],
        ],
        id_type: InstrumentIdType,
        get_id: Callable[[Any], str],
    ):
        get_instruments = get_instruments_of_type(mocked_services.instruments)
        get_instrument_by_cached = get_instrument_of_type_by(instruments_cache)
        get_instruments.assert_called_once()
        (inst,) = random.sample(get_instruments().instruments, k=1)
        get_instruments.reset_mock()
        time.sleep(0.1)

        _ = get_instrument_by_cached(
            id_type=id_type,
            class_code=inst.class_code,
            id=get_id(inst),
        )

        get_instruments.assert_called_once()
