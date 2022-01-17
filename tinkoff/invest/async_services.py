# pylint:disable=redefined-builtin,too-many-lines
from datetime import datetime
from typing import AsyncIterable, List, Optional

from tinkoff.invest.grpc import (
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

from . import grpc_helpers
from .constants import APP_NAME
from .schemas import (
    BondResponse,
    BondsResponse,
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
    GetAccountsRequest,
    GetAccountsResponse,
    GetAccruedInterestsRequest,
    GetAccruedInterestsResponse,
    GetCandlesRequest,
    GetCandlesResponse,
    GetDividendsRequest,
    GetDividendsResponse,
    GetFuturesMarginRequest,
    GetFuturesMarginResponse,
    GetInfoRequest,
    GetInfoResponse,
    GetLastPricesRequest,
    GetLastPricesResponse,
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


class AsyncServices:
    def __init__(self, channel, token: str) -> None:
        metadata = [("authorization", f"Bearer {token}"), ("x-app-name", APP_NAME)]
        self.instruments = InstrumentsService(channel, metadata)
        self.market_data = MarketDataService(channel, metadata)
        self.market_data_stream = MarketDataStreamService(channel, metadata)
        self.operations = OperationsService(channel, metadata)
        self.orders_stream = OrdersStreamService(channel, metadata)
        self.orders = OrdersService(channel, metadata)
        self.users = UsersService(channel, metadata)
        self.sandbox = SandboxService(channel, metadata)
        self.stop_orders = StopOrdersService(channel, metadata)


class InstrumentsService(grpc_helpers.Service):
    _stub_factory = instruments_pb2_grpc.InstrumentsServiceStub

    async def trading_schedules(
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
        response = await self.stub.TradingSchedules(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.TradingSchedulesRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, TradingSchedulesResponse)

    async def bond_by(
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
        response = await self.stub.BondBy(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, BondResponse)

    async def bonds(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> BondsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response = await self.stub.Bonds(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, BondsResponse)

    async def currency_by(
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
        response = await self.stub.CurrencyBy(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, CurrencyResponse)

    async def currencies(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> CurrenciesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response = await self.stub.Currencies(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, CurrenciesResponse)

    async def etf_by(
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
        response = await self.stub.EtfBy(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, EtfResponse)

    async def etfs(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> EtfsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response = await self.stub.Etfs(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, EtfsResponse)

    async def future_by(
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
        response = await self.stub.FutureBy(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, FutureResponse)

    async def futures(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> FuturesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response = await self.stub.Futures(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, FuturesResponse)

    async def share_by(
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
        response = await self.stub.ShareBy(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, ShareResponse)

    async def shares(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> SharesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response = await self.stub.Shares(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, SharesResponse)

    async def get_accrued_interests(
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
        response = await self.stub.GetAccruedInterests(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetAccruedInterestsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetAccruedInterestsResponse)

    async def get_futures_margin(self, *, figi: str = "") -> GetFuturesMarginResponse:
        request = GetFuturesMarginRequest()
        request.figi = figi
        response = await self.stub.GetFuturesMargin(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetFuturesMarginRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetFuturesMarginResponse)

    async def get_instrument_by(
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
        response = await self.stub.GetInstrumentBy(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, InstrumentResponse)

    async def get_dividends(
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
        response = await self.stub.GetDividends(
            request=grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetDividendsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetDividendsResponse)


class MarketDataService(grpc_helpers.Service):
    _stub_factory = marketdata_pb2_grpc.MarketDataServiceStub

    async def get_candles(
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
        response = await self.stub.GetCandles(
            request=grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetCandlesRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetCandlesResponse)

    async def get_last_prices(
        self, *, figi: Optional[List[str]] = None
    ) -> GetLastPricesResponse:
        figi = figi or []

        request = GetLastPricesRequest()
        request.figi = figi
        response = await self.stub.GetLastPrices(
            request=grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetLastPricesRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetLastPricesResponse)

    async def get_order_book(
        self, *, figi: str = "", depth: int = 0
    ) -> GetOrderBookResponse:
        request = GetOrderBookRequest()
        request.figi = figi
        request.depth = depth
        response = await self.stub.GetOrderBook(
            request=grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetOrderBookRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetOrderBookResponse)

    async def get_trading_status(self, *, figi: str = "") -> GetTradingStatusResponse:
        request = GetTradingStatusRequest()
        request.figi = figi
        response = await self.stub.GetTradingStatus(
            request=grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetTradingStatusRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetTradingStatusResponse)


class MarketDataStreamService(grpc_helpers.Service):
    _stub_factory = marketdata_pb2_grpc.MarketDataStreamServiceStub

    @staticmethod
    async def _convert_market_data_stream_request(
        request_iterator: AsyncIterable[MarketDataRequest],
    ) -> AsyncIterable[marketdata_pb2.MarketDataRequest]:
        async for request in request_iterator:
            yield grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.MarketDataRequest()
            )

    async def market_data_stream(
        self,
        request_iterator: AsyncIterable[MarketDataRequest],
    ) -> AsyncIterable[MarketDataResponse]:
        async for response in self.stub.MarketDataStream(
            request_iterator=self._convert_market_data_stream_request(request_iterator),
            metadata=self.metadata,
        ):
            yield grpc_helpers.protobuf_to_dataclass(response, MarketDataResponse)


class OperationsService(grpc_helpers.Service):
    _stub_factory = operations_pb2_grpc.OperationsServiceStub

    async def get_operations(
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
        response = await self.stub.GetOperations(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.OperationsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, OperationsResponse)

    async def get_portfolio(self, *, account_id: str = "") -> PortfolioResponse:
        request = PortfolioRequest()
        request.account_id = account_id
        response = await self.stub.GetPortfolio(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PortfolioResponse)

    async def get_positions(self, *, account_id: str = "") -> PositionsResponse:
        request = PositionsRequest()
        request.account_id = account_id
        response = await self.stub.GetPositions(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PositionsResponse)

    async def get_withdraw_limits(
        self, *, account_id: str = ""
    ) -> WithdrawLimitsResponse:
        request = WithdrawLimitsRequest()
        request.account_id = account_id
        response = await self.stub.GetWithdrawLimits(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.WithdrawLimitsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, WithdrawLimitsResponse)


class OrdersStreamService(grpc_helpers.Service):
    _stub_factory = orders_pb2_grpc.OrdersStreamServiceStub

    async def trades_stream(self) -> AsyncIterable[TradesStreamResponse]:
        request = TradesStreamRequest()
        async for response in self.stub.TradesStream(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.WithdrawLimitsRequest()
            ),
            metadata=self.metadata,
        ):
            yield grpc_helpers.protobuf_to_dataclass(response, TradesStreamResponse)


class OrdersService(grpc_helpers.Service):
    _stub_factory = orders_pb2_grpc.OrdersServiceStub

    async def post_order(
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
        response = await self.stub.PostOrder(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.PostOrderRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    async def cancel_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response = await self.stub.CancelOrder(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.CancelOrderRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, CancelOrderResponse)

    async def get_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response = await self.stub.GetOrderState(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrderStateRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, OrderState)

    async def get_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response = await self.stub.GetOrders(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrdersRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetOrdersResponse)


class UsersService(grpc_helpers.Service):
    _stub_factory = users_pb2_grpc.UsersServiceStub

    async def get_accounts(self) -> GetAccountsResponse:
        request = GetAccountsRequest()
        response = await self.stub.GetAccounts(
            request=grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetAccountsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetAccountsResponse)

    async def get_margin_attributes(
        self, *, account_id: str = ""
    ) -> GetMarginAttributesResponse:
        request = GetMarginAttributesRequest()
        request.account_id = account_id
        response = await self.stub.GetMarginAttributes(
            request=grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetMarginAttributesRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetMarginAttributesResponse)

    async def get_user_tariff(self) -> GetUserTariffResponse:
        request = GetUserTariffRequest()
        response = await self.stub.GetUserTariff(
            request=grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetUserTariffRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetUserTariffResponse)

    async def get_info(self) -> GetInfoResponse:
        request = GetInfoRequest()
        response = await self.stub.GetInfo(
            request=grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetInfoRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetInfoResponse)


class SandboxService(grpc_helpers.Service):
    _stub_factory = sandbox_pb2_grpc.SandboxServiceStub

    async def open_sandbox_account(self) -> OpenSandboxAccountResponse:
        request = OpenSandboxAccountRequest()
        response = await self.stub.OpenSandboxAccount(
            request=grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.OpenSandboxAccountRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, OpenSandboxAccountResponse)

    async def get_sandbox_accounts(self) -> GetAccountsResponse:
        request = GetAccountsRequest()
        response = await self.stub.GetSandboxAccounts(
            request=grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetAccountsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetAccountsResponse)

    async def close_sandbox_account(
        self, *, account_id: str = ""
    ) -> CloseSandboxAccountResponse:
        request = CloseSandboxAccountRequest()
        request.account_id = account_id
        response = await self.stub.CloseSandboxAccount(
            request=grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.CloseSandboxAccountRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, CloseSandboxAccountResponse)

    async def post_sandbox_order(
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
        response = await self.stub.PostSandboxOrder(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.PostOrderRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    async def get_sandbox_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response = await self.stub.GetSandboxOrders(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrdersRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetOrdersResponse)

    async def cancel_sandbox_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response = await self.stub.CancelSandboxOrder(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.CancelOrderRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, CancelOrderResponse)

    async def get_sandbox_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response = await self.stub.GetSandboxOrderState(
            request=grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrderStateRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, OrderState)

    async def get_sandbox_positions(self, *, account_id: str = "") -> PositionsResponse:
        request = PositionsRequest()
        request.account_id = account_id
        response = await self.stub.GetSandboxPositions(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PositionsResponse)

    async def get_sandbox_operations(
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
        response = await self.stub.GetSandboxOperations(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.OperationsRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, OperationsResponse)

    async def get_sandbox_portfolio(self, *, account_id: str = "") -> PortfolioResponse:
        request = PortfolioRequest()
        request.account_id = account_id
        response = await self.stub.GetSandboxPortfolio(
            request=grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PortfolioResponse)

    async def sandbox_pay_in(
        self, *, account_id: str = "", amount: Optional[MoneyValue] = None
    ) -> SandboxPayInResponse:
        request = SandboxPayInRequest()
        request.account_id = account_id
        if amount is not None:
            request.amount = amount
        response = await self.stub.SandboxPayIn(
            request=grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.SandboxPayInRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, SandboxPayInResponse)


class StopOrdersService(grpc_helpers.Service):
    _stub_factory = stoporders_pb2_grpc.StopOrdersServiceStub

    async def post_stop_order(
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
        response = await self.stub.PostStopOrder(
            request=grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.PostStopOrderRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, PostStopOrderResponse)

    async def get_stop_orders(self, *, account_id: str = "") -> GetStopOrdersResponse:
        request = GetStopOrdersRequest()
        request.account_id = account_id
        response = await self.stub.GetStopOrders(
            request=grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.GetStopOrdersRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, GetStopOrdersResponse)

    async def cancel_stop_order(
        self, *, account_id: str = "", stop_order_id: str = ""
    ) -> CancelStopOrderResponse:
        request = CancelStopOrderRequest()
        request.account_id = account_id
        request.stop_order_id = stop_order_id
        response = await self.stub.CancelStopOrder(
            request=grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.CancelStopOrderRequest()
            ),
            metadata=self.metadata,
        )
        return grpc_helpers.protobuf_to_dataclass(response, CancelStopOrderResponse)
