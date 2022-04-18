# pylint:disable=redefined-builtin,too-many-lines
from datetime import datetime
from typing import Generator, Iterable, List, Optional

import grpc

from tinkoff.invest.market_data_stream.market_data_stream_manager import (
    MarketDataStreamManager,
)

from . import _grpc_helpers
from ._errors import handle_request_error, handle_request_error_gen
from .grpc import (
    instruments_pb2,
    instruments_pb2_grpc,
    marketdata_pb2,
    marketdata_pb2_grpc,
    operations_pb2,
    operations_pb2_grpc,
    orders_pb2,
    orders_pb2_grpc,
    sandbox_pb2,
    sandbox_pb2_grpc,
    stoporders_pb2,
    stoporders_pb2_grpc,
    users_pb2,
    users_pb2_grpc,
)
from .logging import get_tracking_id_from_call, log_request
from .metadata import get_metadata
from .schemas import (
    AssetRequest,
    AssetResponse,
    AssetsRequest,
    AssetsResponse,
    BondResponse,
    BondsResponse,
    BrokerReportRequest,
    BrokerReportResponse,
    CancelOrderRequest,
    CancelOrderResponse,
    CancelStopOrderRequest,
    CancelStopOrderResponse,
    CandleInterval,
    CloseSandboxAccountRequest,
    CloseSandboxAccountResponse,
    CurrenciesResponse,
    CurrencyResponse,
    EtfResponse,
    EtfsResponse,
    FutureResponse,
    FuturesResponse,
    GenerateBrokerReportRequest,
    GenerateDividendsForeignIssuerReportRequest,
    GetAccountsRequest,
    GetAccountsResponse,
    GetAccruedInterestsRequest,
    GetAccruedInterestsResponse,
    GetBondCouponsRequest,
    GetBondCouponsResponse,
    GetBrokerReportRequest,
    GetCandlesRequest,
    GetCandlesResponse,
    GetDividendsForeignIssuerReportRequest,
    GetDividendsForeignIssuerRequest,
    GetDividendsForeignIssuerResponse,
    GetDividendsRequest,
    GetDividendsResponse,
    GetFuturesMarginRequest,
    GetFuturesMarginResponse,
    GetInfoRequest,
    GetInfoResponse,
    GetLastPricesRequest,
    GetLastPricesResponse,
    GetLastTradesRequest,
    GetLastTradesResponse,
    GetMarginAttributesRequest,
    GetMarginAttributesResponse,
    GetOrderBookRequest,
    GetOrderBookResponse,
    GetOrdersRequest,
    GetOrdersResponse,
    GetOrderStateRequest,
    GetStopOrdersRequest,
    GetStopOrdersResponse,
    GetTradingStatusRequest,
    GetTradingStatusResponse,
    GetUserTariffRequest,
    GetUserTariffResponse,
    HistoricCandle,
    InstrumentIdType,
    InstrumentRequest,
    InstrumentResponse,
    InstrumentsRequest,
    InstrumentStatus,
    MarketDataRequest,
    MarketDataResponse,
    MoneyValue,
    OpenSandboxAccountRequest,
    OpenSandboxAccountResponse,
    OperationsRequest,
    OperationsResponse,
    OperationState,
    OrderDirection,
    OrderState,
    OrderType,
    PortfolioRequest,
    PortfolioResponse,
    PositionsRequest,
    PositionsResponse,
    PostOrderRequest,
    PostOrderResponse,
    PostStopOrderRequest,
    PostStopOrderResponse,
    Quotation,
    SandboxPayInRequest,
    SandboxPayInResponse,
    ShareResponse,
    SharesResponse,
    StopOrderDirection,
    StopOrderExpirationType,
    StopOrderType,
    TradesStreamRequest,
    TradesStreamResponse,
    TradingSchedulesRequest,
    TradingSchedulesResponse,
    WithdrawLimitsRequest,
    WithdrawLimitsResponse,
)
from .typedefs import AccountId
from .utils import get_intervals, now

__all__ = (
    "Services",
    "InstrumentsService",
    "MarketDataService",
    "MarketDataStreamService",
    "OperationsService",
    "OrdersStreamService",
    "OrdersService",
    "UsersService",
    "SandboxService",
    "StopOrdersService",
)


class Services:
    def __init__(
        self, channel: grpc.Channel, token: str, sandbox_token: Optional[str] = None
    ) -> None:
        metadata = get_metadata(token)
        sandbox_metadata = get_metadata(sandbox_token or token)
        self.instruments = InstrumentsService(channel, metadata)
        self.market_data = MarketDataService(channel, metadata)
        self.market_data_stream = MarketDataStreamService(channel, metadata)
        self.operations = OperationsService(channel, metadata)
        self.orders_stream = OrdersStreamService(channel, metadata)
        self.orders = OrdersService(channel, metadata)
        self.users = UsersService(channel, metadata)
        self.sandbox = SandboxService(channel, sandbox_metadata)
        self.stop_orders = StopOrdersService(channel, metadata)

    def create_market_data_stream(self) -> MarketDataStreamManager:
        return MarketDataStreamManager(
            market_data_stream_service=self.market_data_stream
        )

    def cancel_all_orders(self, account_id: AccountId) -> None:
        orders_service: OrdersService = self.orders
        stop_orders_service: StopOrdersService = self.stop_orders

        orders_response = orders_service.get_orders(account_id=account_id)
        for order in orders_response.orders:
            orders_service.cancel_order(account_id=account_id, order_id=order.order_id)

        stop_orders_response = stop_orders_service.get_stop_orders(
            account_id=account_id
        )
        for stop_order in stop_orders_response.stop_orders:
            stop_orders_service.cancel_stop_order(
                account_id=account_id, stop_order_id=stop_order.stop_order_id
            )

    def get_all_candles(
        self,
        *,
        from_: datetime,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
        figi: str = "",
    ) -> Generator[HistoricCandle, None, None]:
        to = to or now()

        for local_from_, local_to in get_intervals(interval, from_, to):
            candles_response = self.market_data.get_candles(
                figi=figi,
                interval=interval,
                from_=local_from_,
                to=local_to,
            )
            yield from candles_response.candles


class InstrumentsService(_grpc_helpers.Service):
    _stub_factory = instruments_pb2_grpc.InstrumentsServiceStub

    @handle_request_error("TradingSchedules")
    def trading_schedules(
        self,
        *,
        exchange: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
    ) -> TradingSchedulesResponse:
        request = TradingSchedulesRequest()
        request.exchange = exchange
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        response, call = self.stub.TradingSchedules.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.TradingSchedulesRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "TradingSchedules")
        return _grpc_helpers.protobuf_to_dataclass(response, TradingSchedulesResponse)

    @handle_request_error("BondBy")
    def bond_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> BondResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response, call = self.stub.BondBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "BondBy")
        return _grpc_helpers.protobuf_to_dataclass(response, BondResponse)

    @handle_request_error("Bonds")
    def bonds(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> BondsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response, call = self.stub.Bonds.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "Bonds")
        return _grpc_helpers.protobuf_to_dataclass(response, BondsResponse)

    @handle_request_error("CurrencyBy")
    def currency_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> CurrencyResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response, call = self.stub.CurrencyBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "CurrencyBy")
        return _grpc_helpers.protobuf_to_dataclass(response, CurrencyResponse)

    @handle_request_error("Currencies")
    def currencies(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> CurrenciesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response, call = self.stub.Currencies.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "Currencies")
        return _grpc_helpers.protobuf_to_dataclass(response, CurrenciesResponse)

    @handle_request_error("EtfBy")
    def etf_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> EtfResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response, call = self.stub.EtfBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "EtfBy")
        return _grpc_helpers.protobuf_to_dataclass(response, EtfResponse)

    @handle_request_error("Etfs")
    def etfs(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> EtfsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response, call = self.stub.Etfs.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "Etfs")
        return _grpc_helpers.protobuf_to_dataclass(response, EtfsResponse)

    @handle_request_error("FutureBy")
    def future_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> FutureResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response, call = self.stub.FutureBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "FutureBy")
        return _grpc_helpers.protobuf_to_dataclass(response, FutureResponse)

    @handle_request_error("Futures")
    def futures(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> FuturesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response, call = self.stub.Futures.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "Futures")
        return _grpc_helpers.protobuf_to_dataclass(response, FuturesResponse)

    @handle_request_error("ShareBy")
    def share_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> ShareResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response, call = self.stub.ShareBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "ShareBy")
        return _grpc_helpers.protobuf_to_dataclass(response, ShareResponse)

    @handle_request_error("Shares")
    def shares(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> SharesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response, call = self.stub.Shares.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "Shares")
        return _grpc_helpers.protobuf_to_dataclass(response, SharesResponse)

    @handle_request_error("GetAccruedInterests")
    def get_accrued_interests(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
    ) -> GetAccruedInterestsResponse:
        request = GetAccruedInterestsRequest()
        request.figi = figi
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        response, call = self.stub.GetAccruedInterests.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetAccruedInterestsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetAccruedInterests")
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetAccruedInterestsResponse
        )

    @handle_request_error("GetFuturesMargin")
    def get_futures_margin(self, *, figi: str = "") -> GetFuturesMarginResponse:
        request = GetFuturesMarginRequest()
        request.figi = figi
        response, call = self.stub.GetFuturesMargin.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetFuturesMarginRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetFuturesMargin")
        return _grpc_helpers.protobuf_to_dataclass(response, GetFuturesMarginResponse)

    @handle_request_error("GetInstrumentBy")
    def get_instrument_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> InstrumentResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response, call = self.stub.GetInstrumentBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetInstrumentBy")
        return _grpc_helpers.protobuf_to_dataclass(response, InstrumentResponse)

    @handle_request_error("GetDividends")
    def get_dividends(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
    ) -> GetDividendsResponse:
        request = GetDividendsRequest()
        request.figi = figi
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        response, call = self.stub.GetDividends.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetDividendsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetDividends")
        return _grpc_helpers.protobuf_to_dataclass(response, GetDividendsResponse)

    @handle_request_error("GetBondCoupons")
    def get_bond_coupons(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
    ) -> GetBondCouponsResponse:
        request = GetBondCouponsRequest()
        request.figi = figi
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        response, call = self.stub.GetBondCoupons.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetBondCouponsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetBondCoupons")
        return _grpc_helpers.protobuf_to_dataclass(response, GetBondCouponsResponse)

    @handle_request_error("GetAssetBy")
    def get_asset_by(
        self,
        *,
        id: str = "",
    ) -> AssetResponse:
        request = AssetRequest()
        request.id = id
        response, call = self.stub.GetAssetBy.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.AssetRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetAssetBy")
        return _grpc_helpers.protobuf_to_dataclass(response, AssetResponse)

    @handle_request_error("GetAssets")
    def get_assets(
        self,
    ) -> AssetsResponse:
        request = AssetsRequest()
        response, call = self.stub.GetAssets.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.AssetsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetAssets")
        return _grpc_helpers.protobuf_to_dataclass(response, AssetsResponse)


class MarketDataService(_grpc_helpers.Service):
    _stub_factory = marketdata_pb2_grpc.MarketDataServiceStub

    @handle_request_error("GetCandles")
    def get_candles(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
    ) -> GetCandlesResponse:
        request = GetCandlesRequest()
        request.figi = figi
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        request.interval = interval
        response, call = self.stub.GetCandles.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetCandlesRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetCandles")
        return _grpc_helpers.protobuf_to_dataclass(response, GetCandlesResponse)

    @handle_request_error("GetLastPrices")
    def get_last_prices(
        self, *, figi: Optional[List[str]] = None
    ) -> GetLastPricesResponse:
        figi = figi or []

        request = GetLastPricesRequest()
        request.figi = figi
        response, call = self.stub.GetLastPrices.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetLastPricesRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetLastPrices")
        return _grpc_helpers.protobuf_to_dataclass(response, GetLastPricesResponse)

    @handle_request_error("GetOrderBook")
    def get_order_book(self, *, figi: str = "", depth: int = 0) -> GetOrderBookResponse:
        request = GetOrderBookRequest()
        request.figi = figi
        request.depth = depth
        response, call = self.stub.GetOrderBook.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetOrderBookRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetOrderBook")
        return _grpc_helpers.protobuf_to_dataclass(response, GetOrderBookResponse)

    @handle_request_error("GetTradingStatus")
    def get_trading_status(self, *, figi: str = "") -> GetTradingStatusResponse:
        request = GetTradingStatusRequest()
        request.figi = figi
        response, call = self.stub.GetTradingStatus.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetTradingStatusRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetTradingStatus")
        return _grpc_helpers.protobuf_to_dataclass(response, GetTradingStatusResponse)

    @handle_request_error("GetLastTrades")
    def get_last_trades(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
    ) -> GetLastTradesResponse:
        request = GetLastTradesRequest()
        request.figi = figi
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        response, call = self.stub.GetLastTrades.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetLastTradesRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetLastTrades")
        return _grpc_helpers.protobuf_to_dataclass(response, GetLastTradesResponse)


class MarketDataStreamService(_grpc_helpers.Service):
    _stub_factory = marketdata_pb2_grpc.MarketDataStreamServiceStub

    @staticmethod
    def _convert_market_data_stream_request(
        request_iterator: Iterable[MarketDataRequest],
    ) -> Iterable[marketdata_pb2.MarketDataRequest]:
        for request in request_iterator:
            yield _grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.MarketDataRequest()
            )

    @handle_request_error_gen("MarketDataStream")
    def market_data_stream(
        self,
        request_iterator: Iterable[MarketDataRequest],
    ) -> Iterable[MarketDataResponse]:
        for response in self.stub.MarketDataStream(
            request_iterator=self._convert_market_data_stream_request(request_iterator),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, MarketDataResponse)


class OperationsService(_grpc_helpers.Service):
    _stub_factory = operations_pb2_grpc.OperationsServiceStub

    @handle_request_error("GetOperations")
    def get_operations(
        self,
        *,
        account_id: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        state: OperationState = OperationState(0),
        figi: str = "",
    ) -> OperationsResponse:
        request = OperationsRequest()
        request.account_id = account_id
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        request.state = state
        request.figi = figi
        response, call = self.stub.GetOperations.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.OperationsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetOperations")
        return _grpc_helpers.protobuf_to_dataclass(response, OperationsResponse)

    @handle_request_error("GetPortfolio")
    def get_portfolio(self, *, account_id: str = "") -> PortfolioResponse:
        request = PortfolioRequest()
        request.account_id = account_id
        response, call = self.stub.GetPortfolio.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetPortfolio")
        return _grpc_helpers.protobuf_to_dataclass(response, PortfolioResponse)

    @handle_request_error("GetPositions")
    def get_positions(self, *, account_id: str = "") -> PositionsResponse:
        request = PositionsRequest()
        request.account_id = account_id
        response, call = self.stub.GetPositions.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetPositions")
        return _grpc_helpers.protobuf_to_dataclass(response, PositionsResponse)

    @handle_request_error("GetWithdrawLimits")
    def get_withdraw_limits(self, *, account_id: str = "") -> WithdrawLimitsResponse:
        request = WithdrawLimitsRequest()
        request.account_id = account_id
        response, call = self.stub.GetWithdrawLimits.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.WithdrawLimitsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetWithdrawLimits")
        return _grpc_helpers.protobuf_to_dataclass(response, WithdrawLimitsResponse)

    @handle_request_error("GetBrokerReport")
    def get_broker_report(
        self,
        *,
        generate_broker_report_request: Optional[GenerateBrokerReportRequest] = None,
        get_broker_report_request: Optional[GetBrokerReportRequest] = None,
    ) -> BrokerReportResponse:
        request = BrokerReportRequest()
        if generate_broker_report_request:
            request.generate_broker_report_request = generate_broker_report_request
        if get_broker_report_request:
            request.get_broker_report_request = get_broker_report_request
        response, call = self.stub.GetBrokerReport.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.BrokerReportRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetBrokerReport")
        return _grpc_helpers.protobuf_to_dataclass(response, BrokerReportResponse)

    @handle_request_error("GetDividendsForeignIssuer")
    def get_dividends_foreign_issuer(
        self,
        *,
        generate_div_foreign_issuer_report: Optional[
            GenerateDividendsForeignIssuerReportRequest
        ] = None,
        get_div_foreign_issuer_report: Optional[
            GetDividendsForeignIssuerReportRequest
        ] = None,
    ) -> GetDividendsForeignIssuerResponse:
        request = GetDividendsForeignIssuerRequest()
        if generate_div_foreign_issuer_report is not None:
            request.generate_div_foreign_issuer_report = (
                generate_div_foreign_issuer_report
            )
        if get_div_foreign_issuer_report is not None:
            request.get_div_foreign_issuer_report = get_div_foreign_issuer_report
        response, call = self.stub.GetDividendsForeignIssuer.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.GetDividendsForeignIssuerRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetDividendsForeignIssuer")
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetDividendsForeignIssuerResponse
        )


class OrdersStreamService(_grpc_helpers.Service):
    _stub_factory = orders_pb2_grpc.OrdersStreamServiceStub

    @handle_request_error_gen("TradesStream")
    def trades_stream(self) -> Iterable[TradesStreamResponse]:
        request = TradesStreamRequest()
        for response in self.stub.TradesStream(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.WithdrawLimitsRequest()
            ),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, TradesStreamResponse)


class OrdersService(_grpc_helpers.Service):
    _stub_factory = orders_pb2_grpc.OrdersServiceStub

    @handle_request_error("PostOrder")
    def post_order(
        self,
        *,
        figi: str = "",
        quantity: int = 0,
        price: Optional[Quotation] = None,
        direction: OrderDirection = OrderDirection(0),
        account_id: str = "",
        order_type: OrderType = OrderType(0),
        order_id: str = "",
    ) -> PostOrderResponse:
        request = PostOrderRequest()
        request.figi = figi
        request.quantity = quantity
        if price is not None:
            request.price = price
        request.direction = direction
        request.account_id = account_id
        request.order_type = order_type
        request.order_id = order_id
        response, call = self.stub.PostOrder.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.PostOrderRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "PostOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    @handle_request_error("CancelOrder")
    def cancel_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response, call = self.stub.CancelOrder.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.CancelOrderRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "CancelOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, CancelOrderResponse)

    @handle_request_error("GetOrderState")
    def get_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response, call = self.stub.GetOrderState.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrderStateRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetOrderState")
        return _grpc_helpers.protobuf_to_dataclass(response, OrderState)

    @handle_request_error("GetOrders")
    def get_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response, call = self.stub.GetOrders.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrdersRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetOrders")
        return _grpc_helpers.protobuf_to_dataclass(response, GetOrdersResponse)


class UsersService(_grpc_helpers.Service):
    _stub_factory = users_pb2_grpc.UsersServiceStub

    @handle_request_error("GetAccounts")
    def get_accounts(self) -> GetAccountsResponse:
        request = GetAccountsRequest()
        response, call = self.stub.GetAccounts.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetAccountsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetAccounts")
        return _grpc_helpers.protobuf_to_dataclass(response, GetAccountsResponse)

    @handle_request_error("GetMarginAttributes")
    def get_margin_attributes(
        self, *, account_id: str = ""
    ) -> GetMarginAttributesResponse:
        request = GetMarginAttributesRequest()
        request.account_id = account_id
        response, call = self.stub.GetMarginAttributes.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetMarginAttributesRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetMarginAttributes")
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetMarginAttributesResponse
        )

    @handle_request_error("GetUserTariff")
    def get_user_tariff(self) -> GetUserTariffResponse:
        request = GetUserTariffRequest()
        response, call = self.stub.GetUserTariff.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetUserTariffRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetUserTariff")
        return _grpc_helpers.protobuf_to_dataclass(response, GetUserTariffResponse)

    @handle_request_error("GetInfo")
    def get_info(self) -> GetInfoResponse:
        request = GetInfoRequest()
        response, call = self.stub.GetInfo.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetInfoRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetInfo")
        return _grpc_helpers.protobuf_to_dataclass(response, GetInfoResponse)


class SandboxService(_grpc_helpers.Service):
    _stub_factory = sandbox_pb2_grpc.SandboxServiceStub

    @handle_request_error("OpenSandboxAccount")
    def open_sandbox_account(self) -> OpenSandboxAccountResponse:
        request = OpenSandboxAccountRequest()
        response, call = self.stub.OpenSandboxAccount.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.OpenSandboxAccountRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "OpenSandboxAccount")
        return _grpc_helpers.protobuf_to_dataclass(response, OpenSandboxAccountResponse)

    @handle_request_error("GetSandboxAccounts")
    def get_sandbox_accounts(self) -> GetAccountsResponse:
        request = GetAccountsRequest()
        response, call = self.stub.GetSandboxAccounts.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetAccountsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetSandboxAccounts")
        return _grpc_helpers.protobuf_to_dataclass(response, GetAccountsResponse)

    @handle_request_error("CloseSandboxAccount")
    def close_sandbox_account(
        self, *, account_id: str = ""
    ) -> CloseSandboxAccountResponse:
        request = CloseSandboxAccountRequest()
        request.account_id = account_id
        response, call = self.stub.CloseSandboxAccount.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.CloseSandboxAccountRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "CloseSandboxAccount")
        return _grpc_helpers.protobuf_to_dataclass(
            response, CloseSandboxAccountResponse
        )

    @handle_request_error("PostSandboxOrder")
    def post_sandbox_order(
        self,
        *,
        figi: str = "",
        quantity: int = 0,
        price: Optional[Quotation] = None,
        direction: OrderDirection = OrderDirection(0),
        account_id: str = "",
        order_type: OrderType = OrderType(0),
        order_id: str = "",
    ) -> PostOrderResponse:
        request = PostOrderRequest()
        request.figi = figi
        request.quantity = quantity
        if price is not None:
            request.price = price
        request.direction = direction
        request.account_id = account_id
        request.order_type = order_type
        request.order_id = order_id
        response, call = self.stub.PostSandboxOrder.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.PostOrderRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "PostSandboxOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    @handle_request_error("GetSandboxOrders")
    def get_sandbox_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response, call = self.stub.GetSandboxOrders.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrdersRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetSandboxOrders")
        return _grpc_helpers.protobuf_to_dataclass(response, GetOrdersResponse)

    @handle_request_error("CancelSandboxOrder")
    def cancel_sandbox_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response, call = self.stub.CancelSandboxOrder.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.CancelOrderRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "CancelSandboxOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, CancelOrderResponse)

    @handle_request_error("GetSandboxOrderState")
    def get_sandbox_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response, call = self.stub.GetSandboxOrderState.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrderStateRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetSandboxOrderState")
        return _grpc_helpers.protobuf_to_dataclass(response, OrderState)

    @handle_request_error("GetSandboxPositions")
    def get_sandbox_positions(self, *, account_id: str = "") -> PositionsResponse:
        request = PositionsRequest()
        request.account_id = account_id
        response, call = self.stub.GetSandboxPositions.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetSandboxPositions")
        return _grpc_helpers.protobuf_to_dataclass(response, PositionsResponse)

    @handle_request_error("GetSandboxOperations")
    def get_sandbox_operations(
        self,
        *,
        account_id: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        state: OperationState = OperationState(0),
        figi: str = "",
    ) -> OperationsResponse:
        request = OperationsRequest()
        request.account_id = account_id
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        request.state = state
        request.figi = figi
        response, call = self.stub.GetSandboxOperations.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.OperationsRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetSandboxOperations")
        return _grpc_helpers.protobuf_to_dataclass(response, OperationsResponse)

    @handle_request_error("GetSandboxPortfolio")
    def get_sandbox_portfolio(self, *, account_id: str = "") -> PortfolioResponse:
        request = PortfolioRequest()
        request.account_id = account_id
        response, call = self.stub.GetSandboxPortfolio.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetSandboxPortfolio")
        return _grpc_helpers.protobuf_to_dataclass(response, PortfolioResponse)

    @handle_request_error("SandboxPayIn")
    def sandbox_pay_in(
        self, *, account_id: str = "", amount: Optional[MoneyValue] = None
    ) -> SandboxPayInResponse:
        request = SandboxPayInRequest()
        request.account_id = account_id
        if amount is not None:
            request.amount = amount
        response, call = self.stub.SandboxPayIn.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.SandboxPayInRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "SandboxPayIn")
        return _grpc_helpers.protobuf_to_dataclass(response, SandboxPayInResponse)


class StopOrdersService(_grpc_helpers.Service):
    _stub_factory = stoporders_pb2_grpc.StopOrdersServiceStub

    @handle_request_error("PostStopOrder")
    def post_stop_order(
        self,
        *,
        figi: str = "",
        quantity: int = 0,
        price: Optional[Quotation] = None,
        stop_price: Optional[Quotation] = None,
        direction: StopOrderDirection = StopOrderDirection(0),
        account_id: str = "",
        expiration_type: StopOrderExpirationType = StopOrderExpirationType(0),
        stop_order_type: StopOrderType = StopOrderType(0),
        expire_date: Optional[datetime] = None,
    ) -> PostStopOrderResponse:
        request = PostStopOrderRequest()
        request.figi = figi
        request.quantity = quantity
        if price is not None:
            request.price = price
        if stop_price is not None:
            request.stop_price = stop_price
        request.direction = direction
        request.account_id = account_id
        request.expiration_type = expiration_type
        request.stop_order_type = stop_order_type
        if expire_date is not None:
            request.expire_date = expire_date
        response, call = self.stub.PostStopOrder.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.PostStopOrderRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "PostStopOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostStopOrderResponse)

    @handle_request_error("GetStopOrders")
    def get_stop_orders(self, *, account_id: str = "") -> GetStopOrdersResponse:
        request = GetStopOrdersRequest()
        request.account_id = account_id
        response, call = self.stub.GetStopOrders.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.GetStopOrdersRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetStopOrders")
        return _grpc_helpers.protobuf_to_dataclass(response, GetStopOrdersResponse)

    @handle_request_error("CancelStopOrder")
    def cancel_stop_order(
        self, *, account_id: str = "", stop_order_id: str = ""
    ) -> CancelStopOrderResponse:
        request = CancelStopOrderRequest()
        request.account_id = account_id
        request.stop_order_id = stop_order_id
        response, call = self.stub.CancelStopOrder.with_call(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.CancelStopOrderRequest()
            ),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "CancelStopOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, CancelStopOrderResponse)
