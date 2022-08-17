import abc

from tinkoff.invest import (
    BondResponse,
    BondsResponse,
    CurrenciesResponse,
    CurrencyResponse,
    EtfResponse,
    EtfsResponse,
    FutureResponse,
    FuturesResponse,
    InstrumentIdType,
    InstrumentStatus,
    ShareResponse,
    SharesResponse,
)


class IInstrumentsGetter(abc.ABC):
    @abc.abstractmethod
    def shares(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> SharesResponse:
        pass

    @abc.abstractmethod
    def share_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> ShareResponse:
        pass

    @abc.abstractmethod
    def futures(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> FuturesResponse:
        pass

    @abc.abstractmethod
    def future_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> FutureResponse:
        pass

    @abc.abstractmethod
    def etfs(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> EtfsResponse:
        pass

    @abc.abstractmethod
    def etf_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> EtfResponse:
        pass

    @abc.abstractmethod
    def bonds(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> BondsResponse:
        pass

    @abc.abstractmethod
    def bond_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> BondResponse:
        pass

    @abc.abstractmethod
    def currencies(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> CurrenciesResponse:
        pass

    @abc.abstractmethod
    def currency_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> CurrencyResponse:
        pass
