# pylint:disable=redefined-builtin,too-many-lines
import asyncio
from datetime import datetime
from typing import AsyncGenerator, AsyncIterable, List, Optional

import grpc

from . import _grpc_helpers
from ._errors import handle_aio_request_error, handle_aio_request_error_gen
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
from .logging import get_tracking_id_from_coro, log_request
from .market_data_stream.async_market_data_stream_manager import (
    AsyncMarketDataStreamManager,
)
from .metadata import get_metadata
from .schemas import (
    AssetRequest,
    AssetResponse,
    AssetsRequest,
    AssetsResponse,
    BondResponse,
    BondsResponse,
    Brand,
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
    EditFavoritesActionType,
    EditFavoritesRequest,
    EditFavoritesRequestInstrument,
    EditFavoritesResponse,
    EtfResponse,
    EtfsResponse,
    FindInstrumentRequest,
    FindInstrumentResponse,
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
    GetBrandRequest,
    GetBrandsRequest,
    GetBrandsResponse,
    GetBrokerReportRequest,
    GetCandlesRequest,
    GetCandlesResponse,
    GetClosePricesRequest,
    GetClosePricesResponse,
    GetCountriesRequest,
    GetCountriesResponse,
    GetDividendsForeignIssuerReportRequest,
    GetDividendsForeignIssuerRequest,
    GetDividendsForeignIssuerResponse,
    GetDividendsRequest,
    GetDividendsResponse,
    GetFavoritesRequest,
    GetFavoritesResponse,
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
    GetOperationsByCursorRequest,
    GetOperationsByCursorResponse,
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
    InstrumentClosePriceRequest,
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
    OptionResponse,
    OptionsResponse,
    OrderDirection,
    OrderState,
    OrderType,
    PortfolioRequest,
    PortfolioResponse,
    PortfolioStreamRequest,
    PortfolioStreamResponse,
    PositionsRequest,
    PositionsResponse,
    PositionsStreamRequest,
    PositionsStreamResponse,
    PostOrderRequest,
    PostOrderResponse,
    PostStopOrderRequest,
    PostStopOrderResponse,
    Quotation,
    ReplaceOrderRequest,
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
    "AsyncServices",
    "InstrumentsService",
    "MarketDataService",
    "MarketDataStreamService",
    "OperationsService",
    "OperationsStreamService",
    "OrdersStreamService",
    "OrdersService",
    "UsersService",
    "SandboxService",
    "StopOrdersService",
)


class AsyncServices:
    def __init__(
        self,
        channel: grpc.aio.Channel,
        token: str,
        sandbox_token: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> None:
        metadata = get_metadata(token, app_name)
        sandbox_metadata = get_metadata(sandbox_token or token, app_name)
        self.instruments = InstrumentsService(channel, metadata)
        self.market_data = MarketDataService(channel, metadata)
        self.market_data_stream = MarketDataStreamService(channel, metadata)
        self.operations = OperationsService(channel, metadata)
        self.operations_stream = OperationsStreamService(channel, metadata)
        self.orders_stream = OrdersStreamService(channel, metadata)
        self.orders = OrdersService(channel, metadata)
        self.users = UsersService(channel, metadata)
        self.sandbox = SandboxService(channel, sandbox_metadata)
        self.stop_orders = StopOrdersService(channel, metadata)

    def create_market_data_stream(self) -> AsyncMarketDataStreamManager:
        return AsyncMarketDataStreamManager(market_data_stream=self.market_data_stream)

    async def cancel_all_orders(self, account_id: AccountId) -> None:
        orders_service: OrdersService = self.orders
        stop_orders_service: StopOrdersService = self.stop_orders

        orders_response = await orders_service.get_orders(account_id=account_id)
        await asyncio.gather(
            *[
                orders_service.cancel_order(
                    account_id=account_id, order_id=order.order_id
                )
                for order in orders_response.orders
            ]
        )

        stop_orders_response = await stop_orders_service.get_stop_orders(
            account_id=account_id
        )
        await asyncio.gather(
            *[
                stop_orders_service.cancel_stop_order(
                    account_id=account_id, stop_order_id=stop_order.stop_order_id
                )
                for stop_order in stop_orders_response.stop_orders
            ]
        )

    async def get_all_candles(
        self,
        *,
        from_: datetime,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
        figi: str = "",
    ) -> AsyncGenerator[HistoricCandle, None]:
        to = to or now()

        for local_from_, local_to in get_intervals(interval, from_, to):
            candles_response = await self.market_data.get_candles(
                figi=figi,
                interval=interval,
                from_=local_from_,
                to=local_to,
            )
            for candle in candles_response.candles:
                yield candle


class InstrumentsService(_grpc_helpers.Service):
    _stub_factory = instruments_pb2_grpc.InstrumentsServiceStub

    @handle_aio_request_error("TradingSchedules")
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
        response_coro = self.stub.TradingSchedules(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.TradingSchedulesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "TradingSchedules")
        return _grpc_helpers.protobuf_to_dataclass(response, TradingSchedulesResponse)

    @handle_aio_request_error("BondBy")
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
        response_coro = self.stub.BondBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "BondBy")
        return _grpc_helpers.protobuf_to_dataclass(response, BondResponse)

    @handle_aio_request_error("Bonds")
    async def bonds(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> BondsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response_coro = self.stub.Bonds(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "Bonds")
        return _grpc_helpers.protobuf_to_dataclass(response, BondsResponse)

    @handle_aio_request_error("CurrencyBy")
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
        response_coro = self.stub.CurrencyBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "CurrencyBy")
        return _grpc_helpers.protobuf_to_dataclass(response, CurrencyResponse)

    @handle_aio_request_error("Currencies")
    async def currencies(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> CurrenciesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response_coro = self.stub.Currencies(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "Currencies")
        return _grpc_helpers.protobuf_to_dataclass(response, CurrenciesResponse)

    @handle_aio_request_error("EtfBy")
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
        response_coro = self.stub.EtfBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "EtfBy")
        return _grpc_helpers.protobuf_to_dataclass(response, EtfResponse)

    @handle_aio_request_error("Etfs")
    async def etfs(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> EtfsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response_coro = self.stub.Etfs(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "Etfs")
        return _grpc_helpers.protobuf_to_dataclass(response, EtfsResponse)

    @handle_aio_request_error("FutureBy")
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
        response_coro = self.stub.FutureBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "FutureBy")
        return _grpc_helpers.protobuf_to_dataclass(response, FutureResponse)

    @handle_aio_request_error("Futures")
    async def futures(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> FuturesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response_coro = self.stub.Futures(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "Futures")
        return _grpc_helpers.protobuf_to_dataclass(response, FuturesResponse)

    @handle_aio_request_error("OptionBy")
    async def option_by(
        self,
        *,
        id_type: InstrumentIdType = InstrumentIdType(0),
        class_code: str = "",
        id: str = "",
    ) -> OptionResponse:
        request = InstrumentRequest()
        request.id_type = id_type
        request.class_code = class_code
        request.id = id
        response_coro = self.stub.OptionBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "OptionBy")
        return _grpc_helpers.protobuf_to_dataclass(response, OptionResponse)

    @handle_aio_request_error("Options")
    async def options(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> OptionsResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response_coro = self.stub.Options(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "Options")
        return _grpc_helpers.protobuf_to_dataclass(response, OptionsResponse)

    @handle_aio_request_error("ShareBy")
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
        response_coro = self.stub.ShareBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "ShareBy")
        return _grpc_helpers.protobuf_to_dataclass(response, ShareResponse)

    @handle_aio_request_error("Shares")
    async def shares(
        self, *, instrument_status: InstrumentStatus = InstrumentStatus(0)
    ) -> SharesResponse:
        request = InstrumentsRequest()
        request.instrument_status = instrument_status
        response_coro = self.stub.Shares(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "Shares")
        return _grpc_helpers.protobuf_to_dataclass(response, SharesResponse)

    @handle_aio_request_error("GetAccruedInterests")
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
        response_coro = self.stub.GetAccruedInterests(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetAccruedInterestsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetAccruedInterests"
        )
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetAccruedInterestsResponse
        )

    @handle_aio_request_error("GetFuturesMargin")
    async def get_futures_margin(self, *, figi: str = "") -> GetFuturesMarginResponse:
        request = GetFuturesMarginRequest()
        request.figi = figi
        response_coro = self.stub.GetFuturesMargin(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetFuturesMarginRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetFuturesMargin")
        return _grpc_helpers.protobuf_to_dataclass(response, GetFuturesMarginResponse)

    @handle_aio_request_error("GetInstrumentBy")
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
        response_coro = self.stub.GetInstrumentBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.InstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetInstrumentBy")
        return _grpc_helpers.protobuf_to_dataclass(response, InstrumentResponse)

    @handle_aio_request_error("GetDividends")
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
        response_coro = self.stub.GetDividends(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetDividendsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetDividends")
        return _grpc_helpers.protobuf_to_dataclass(response, GetDividendsResponse)

    @handle_aio_request_error("GetBondCoupons")
    async def get_bond_coupons(
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
        response_coro = self.stub.GetBondCoupons(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetBondCouponsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetBondCoupons")
        return _grpc_helpers.protobuf_to_dataclass(response, GetBondCouponsResponse)

    @handle_aio_request_error("GetAssetBy")
    async def get_asset_by(
        self,
        *,
        id: str = "",
    ) -> AssetResponse:
        request = AssetRequest()
        request.id = id
        response_coro = self.stub.GetAssetBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.AssetRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetAssetBy")
        return _grpc_helpers.protobuf_to_dataclass(response, AssetResponse)

    @handle_aio_request_error("GetAssets")
    async def get_assets(
        self,
    ) -> AssetsResponse:
        request = AssetsRequest()
        response_coro = self.stub.GetAssets(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.AssetsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetAssets")
        return _grpc_helpers.protobuf_to_dataclass(response, AssetsResponse)

    @handle_aio_request_error("GetFavorites")
    async def get_favorites(
        self,
    ) -> GetFavoritesResponse:
        request = GetFavoritesRequest()
        response_coro = self.stub.GetFavorites(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetFavoritesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetFavorites")
        return _grpc_helpers.protobuf_to_dataclass(response, GetFavoritesResponse)

    @handle_aio_request_error("EditFavorites")
    async def edit_favorites(
        self,
        *,
        instruments: Optional[List[EditFavoritesRequestInstrument]] = None,
        action_type: Optional[EditFavoritesActionType] = None,
    ) -> EditFavoritesResponse:
        request = EditFavoritesRequest()
        if action_type is not None:
            request.action_type = action_type
        if instruments is not None:
            request.instruments = instruments
        response_coro = self.stub.EditFavorites(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.EditFavoritesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "EditFavorites")
        return _grpc_helpers.protobuf_to_dataclass(response, EditFavoritesResponse)

    @handle_aio_request_error("GetCountries")
    async def get_countries(
        self,
    ) -> GetCountriesResponse:
        request = GetCountriesRequest()
        response_coro = self.stub.GetCountries(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetCountriesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetCountries")
        return _grpc_helpers.protobuf_to_dataclass(response, GetCountriesResponse)

    @handle_aio_request_error("FindInstrument")
    async def find_instrument(self, *, query: str = "") -> FindInstrumentResponse:
        request = FindInstrumentRequest()
        request.query = query
        response_coro = self.stub.FindInstrument(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.FindInstrumentRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "FindInstrument")
        return _grpc_helpers.protobuf_to_dataclass(response, FindInstrumentResponse)

    @handle_aio_request_error("GetBrands")
    async def get_brands(
        self,
    ) -> GetBrandsResponse:
        request = GetBrandsRequest()
        response_coro = self.stub.GetBrands(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetBrandsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetBrands")
        return _grpc_helpers.protobuf_to_dataclass(response, GetBrandsResponse)

    @handle_aio_request_error("GetBrandBy")
    async def get_brands_by(self, id: str = "") -> Brand:
        request = GetBrandRequest()
        request.id = id
        response_coro = self.stub.GetBrandBy(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, instruments_pb2.GetBrandRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetBrandBy")
        return _grpc_helpers.protobuf_to_dataclass(response, Brand)


class MarketDataService(_grpc_helpers.Service):
    _stub_factory = marketdata_pb2_grpc.MarketDataServiceStub

    @handle_aio_request_error("GetCandles")
    async def get_candles(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        interval: CandleInterval = CandleInterval(0),
        instrument_id: str = "",
    ) -> GetCandlesResponse:
        request = GetCandlesRequest()
        request.figi = figi
        request.instrument_id = instrument_id
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        request.interval = interval
        response_coro = self.stub.GetCandles(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetCandlesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetCandles")
        return _grpc_helpers.protobuf_to_dataclass(response, GetCandlesResponse)

    @handle_aio_request_error("GetLastPrices")
    async def get_last_prices(
        self,
        *,
        figi: Optional[List[str]] = None,
        instrument_id: Optional[List[str]] = None,
    ) -> GetLastPricesResponse:
        figi = figi or []
        instrument_id = instrument_id or []

        request = GetLastPricesRequest()
        request.figi = figi
        request.instrument_id = instrument_id
        response_coro = self.stub.GetLastPrices(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetLastPricesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetLastPrices")
        return _grpc_helpers.protobuf_to_dataclass(response, GetLastPricesResponse)

    @handle_aio_request_error("GetOrderBook")
    async def get_order_book(
        self, *, figi: str = "", depth: int = 0, instrument_id: str = ""
    ) -> GetOrderBookResponse:
        request = GetOrderBookRequest()
        request.figi = figi
        request.instrument_id = instrument_id
        request.depth = depth
        response_coro = self.stub.GetOrderBook(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetOrderBookRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetOrderBook")
        return _grpc_helpers.protobuf_to_dataclass(response, GetOrderBookResponse)

    @handle_aio_request_error("GetTradingStatus")
    async def get_trading_status(
        self, *, figi: str = "", instrument_id: str = ""
    ) -> GetTradingStatusResponse:
        request = GetTradingStatusRequest()
        request.figi = figi
        request.instrument_id = instrument_id
        response_coro = self.stub.GetTradingStatus(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetTradingStatusRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetTradingStatus")
        return _grpc_helpers.protobuf_to_dataclass(response, GetTradingStatusResponse)

    @handle_aio_request_error("GetLastTrades")
    async def get_last_trades(
        self,
        *,
        figi: str = "",
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        instrument_id: str = "",
    ) -> GetLastTradesResponse:
        request = GetLastTradesRequest()
        request.figi = figi
        request.instrument_id = instrument_id
        if from_ is not None:
            request.from_ = from_
        if to is not None:
            request.to = to
        response_coro = self.stub.GetLastTrades(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetLastTradesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetLastTrades")
        return _grpc_helpers.protobuf_to_dataclass(response, GetLastTradesResponse)

    @handle_aio_request_error("GetClosePrices")
    async def get_close_prices(
        self,
        *,
        instruments: Optional[List[InstrumentClosePriceRequest]] = None,
    ) -> GetClosePricesResponse:
        request = GetClosePricesRequest()
        if instruments:
            request.instruments = instruments
        response_coro = self.stub.GetClosePrices(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.GetClosePricesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetClosePrices")
        return _grpc_helpers.protobuf_to_dataclass(response, GetClosePricesResponse)


class MarketDataStreamService(_grpc_helpers.Service):
    _stub_factory = marketdata_pb2_grpc.MarketDataStreamServiceStub

    @staticmethod
    async def _convert_market_data_stream_request(
        request_iterator: AsyncIterable[MarketDataRequest],
    ) -> AsyncIterable[marketdata_pb2.MarketDataRequest]:
        async for request in request_iterator:
            yield _grpc_helpers.dataclass_to_protobuff(
                request, marketdata_pb2.MarketDataRequest()
            )

    @handle_aio_request_error_gen("MarketDataStream")
    async def market_data_stream(
        self,
        request_iterator: AsyncIterable[MarketDataRequest],
    ) -> AsyncIterable[MarketDataResponse]:
        async for response in self.stub.MarketDataStream(
            request_iterator=self._convert_market_data_stream_request(request_iterator),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, MarketDataResponse)


class OperationsService(_grpc_helpers.Service):
    _stub_factory = operations_pb2_grpc.OperationsServiceStub

    @handle_aio_request_error("GetOperations")
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
        response_coro = self.stub.GetOperations(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.OperationsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetOperations")
        return _grpc_helpers.protobuf_to_dataclass(response, OperationsResponse)

    @handle_aio_request_error("GetPortfolio")
    async def get_portfolio(self, *, account_id: str = "") -> PortfolioResponse:
        request = PortfolioRequest()
        request.account_id = account_id
        response_coro = self.stub.GetPortfolio(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetPortfolio")
        return _grpc_helpers.protobuf_to_dataclass(response, PortfolioResponse)

    @handle_aio_request_error("GetPositions")
    async def get_positions(self, *, account_id: str = "") -> PositionsResponse:
        request = PositionsRequest()
        request.account_id = account_id
        response_coro = self.stub.GetPositions(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetPositions")
        return _grpc_helpers.protobuf_to_dataclass(response, PositionsResponse)

    @handle_aio_request_error("GetWithdrawLimits")
    async def get_withdraw_limits(
        self, *, account_id: str = ""
    ) -> WithdrawLimitsResponse:
        request = WithdrawLimitsRequest()
        request.account_id = account_id
        response_coro = self.stub.GetWithdrawLimits(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.WithdrawLimitsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetWithdrawLimits")
        return _grpc_helpers.protobuf_to_dataclass(response, WithdrawLimitsResponse)

    @handle_aio_request_error("GetBrokerReport")
    async def get_broker_report(
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
        response_coro = self.stub.GetBrokerReport(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.BrokerReportRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetBrokerReport")
        return _grpc_helpers.protobuf_to_dataclass(response, BrokerReportResponse)

    @handle_aio_request_error("GetDividendsForeignIssuer")
    async def get_dividends_foreign_issuer(
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
        response_coro = self.stub.GetDividendsForeignIssuer(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.GetDividendsForeignIssuerRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetDividendsForeignIssuer"
        )
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetDividendsForeignIssuerResponse
        )

    @handle_aio_request_error("GetOperationsByCursor")
    async def get_operations_by_cursor(
        self,
        request: GetOperationsByCursorRequest,
    ) -> GetOperationsByCursorResponse:
        response_coro = self.stub.GetOperationsByCursor(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.GetOperationsByCursorRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetOperationsByCursor"
        )
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetOperationsByCursorResponse
        )


class OperationsStreamService(_grpc_helpers.Service):
    _stub_factory = operations_pb2_grpc.OperationsStreamServiceStub

    @handle_aio_request_error_gen("PortfolioStream")
    async def portfolio_stream(
        self, *, accounts: Optional[List[str]] = None
    ) -> AsyncIterable[PortfolioStreamResponse]:
        request = PortfolioStreamRequest()
        if accounts:
            request.accounts = accounts
        else:
            raise ValueError("accounts can not be empty")
        async for response in self.stub.PortfolioStream(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioStreamRequest()
            ),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, PortfolioStreamResponse)

    @handle_aio_request_error_gen("PositionsStream")
    async def positions_stream(
        self, *, accounts: Optional[List[str]] = None
    ) -> AsyncIterable[PositionsStreamResponse]:
        request = PositionsStreamRequest()
        if accounts:
            request.accounts = accounts
        else:
            raise ValueError("accounts can not be empty")
        async for response in self.stub.PositionsStream(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsStreamRequest()
            ),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, PositionsStreamResponse)


class OrdersStreamService(_grpc_helpers.Service):
    _stub_factory = orders_pb2_grpc.OrdersStreamServiceStub

    @handle_aio_request_error_gen("TradesStream")
    async def trades_stream(
        self, *, accounts: Optional[List[str]] = None
    ) -> AsyncIterable[TradesStreamResponse]:
        request = TradesStreamRequest()
        if accounts:
            request.accounts = accounts
        else:
            raise ValueError("accounts can not be empty")
        async for response in self.stub.TradesStream(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.TradesStreamRequest()
            ),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, TradesStreamResponse)


class OrdersService(_grpc_helpers.Service):
    _stub_factory = orders_pb2_grpc.OrdersServiceStub

    @handle_aio_request_error("PostOrder")
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
        response_coro = self.stub.PostOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.PostOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "PostOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    @handle_aio_request_error("CancelOrder")
    async def cancel_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response_coro = self.stub.CancelOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.CancelOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "CancelOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, CancelOrderResponse)

    @handle_aio_request_error("GetOrderState")
    async def get_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response_coro = self.stub.GetOrderState(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrderStateRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetOrderState")
        return _grpc_helpers.protobuf_to_dataclass(response, OrderState)

    @handle_aio_request_error("GetOrders")
    async def get_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response_coro = self.stub.GetOrders(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrdersRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetOrders")
        return _grpc_helpers.protobuf_to_dataclass(response, GetOrdersResponse)

    @handle_aio_request_error("ReplaceOrder")
    async def replace_order(self, request: ReplaceOrderRequest) -> PostOrderResponse:
        response_coro = self.stub.ReplaceOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.ReplaceOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "ReplaceOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)


class UsersService(_grpc_helpers.Service):
    _stub_factory = users_pb2_grpc.UsersServiceStub

    @handle_aio_request_error("GetAccounts")
    async def get_accounts(self) -> GetAccountsResponse:
        request = GetAccountsRequest()
        response_coro = self.stub.GetAccounts(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetAccountsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetAccounts")
        return _grpc_helpers.protobuf_to_dataclass(response, GetAccountsResponse)

    @handle_aio_request_error("GetMarginAttributes")
    async def get_margin_attributes(
        self, *, account_id: str = ""
    ) -> GetMarginAttributesResponse:
        request = GetMarginAttributesRequest()
        request.account_id = account_id
        response_coro = self.stub.GetMarginAttributes(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetMarginAttributesRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetMarginAttributes"
        )
        return _grpc_helpers.protobuf_to_dataclass(
            response, GetMarginAttributesResponse
        )

    @handle_aio_request_error("GetUserTariff")
    async def get_user_tariff(self) -> GetUserTariffResponse:
        request = GetUserTariffRequest()
        response_coro = self.stub.GetUserTariff(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetUserTariffRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetUserTariff")
        return _grpc_helpers.protobuf_to_dataclass(response, GetUserTariffResponse)

    @handle_aio_request_error("GetInfo")
    async def get_info(self) -> GetInfoResponse:
        request = GetInfoRequest()
        response_coro = self.stub.GetInfo(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetInfoRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetInfo")
        return _grpc_helpers.protobuf_to_dataclass(response, GetInfoResponse)


class SandboxService(_grpc_helpers.Service):
    _stub_factory = sandbox_pb2_grpc.SandboxServiceStub

    @handle_aio_request_error("OpenSandboxAccount")
    async def open_sandbox_account(self) -> OpenSandboxAccountResponse:
        request = OpenSandboxAccountRequest()
        response_coro = self.stub.OpenSandboxAccount(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.OpenSandboxAccountRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "OpenSandboxAccount"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, OpenSandboxAccountResponse)

    @handle_aio_request_error("GetSandboxAccounts")
    async def get_sandbox_accounts(self) -> GetAccountsResponse:
        request = GetAccountsRequest()
        response_coro = self.stub.GetSandboxAccounts(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, users_pb2.GetAccountsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetSandboxAccounts"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, GetAccountsResponse)

    @handle_aio_request_error("CloseSandboxAccount")
    async def close_sandbox_account(
        self, *, account_id: str = ""
    ) -> CloseSandboxAccountResponse:
        request = CloseSandboxAccountRequest()
        request.account_id = account_id
        response_coro = self.stub.CloseSandboxAccount(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.CloseSandboxAccountRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "CloseSandboxAccount"
        )
        return _grpc_helpers.protobuf_to_dataclass(
            response, CloseSandboxAccountResponse
        )

    @handle_aio_request_error("PostSandboxOrder")
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
        response_coro = self.stub.PostSandboxOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.PostOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "PostSandboxOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    @handle_aio_request_error("ReplaceSandboxOrder")
    async def replace_sandbox_order(
        self,
        request: "ReplaceOrderRequest",
    ) -> PostOrderResponse:
        response_coro = self.stub.ReplaceSandboxOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.ReplaceOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "ReplaceSandboxOrder"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, PostOrderResponse)

    @handle_aio_request_error("GetSandboxOrders")
    async def get_sandbox_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response_coro = self.stub.GetSandboxOrders(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrdersRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetSandboxOrders")
        return _grpc_helpers.protobuf_to_dataclass(response, GetOrdersResponse)

    @handle_aio_request_error("CancelSandboxOrder")
    async def cancel_sandbox_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response_coro = self.stub.CancelSandboxOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.CancelOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "CancelSandboxOrder"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, CancelOrderResponse)

    @handle_aio_request_error("GetSandboxOrderState")
    async def get_sandbox_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response_coro = self.stub.GetSandboxOrderState(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.GetOrderStateRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetSandboxOrderState"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, OrderState)

    @handle_aio_request_error("GetSandboxPositions")
    async def get_sandbox_positions(self, *, account_id: str = "") -> PositionsResponse:
        request = PositionsRequest()
        request.account_id = account_id
        response_coro = self.stub.GetSandboxPositions(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PositionsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetSandboxPositions"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, PositionsResponse)

    @handle_aio_request_error("GetSandboxOperations")
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
        response_coro = self.stub.GetSandboxOperations(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.OperationsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetSandboxOperations"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, OperationsResponse)

    @handle_aio_request_error("GetSandboxPortfolio")
    async def get_sandbox_portfolio(self, *, account_id: str = "") -> PortfolioResponse:
        request = PortfolioRequest()
        request.account_id = account_id
        response_coro = self.stub.GetSandboxPortfolio(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.PortfolioRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetSandboxPortfolio"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, PortfolioResponse)

    @handle_aio_request_error("SandboxPayIn")
    async def sandbox_pay_in(
        self, *, account_id: str = "", amount: Optional[MoneyValue] = None
    ) -> SandboxPayInResponse:
        request = SandboxPayInRequest()
        request.account_id = account_id
        if amount is not None:
            request.amount = amount
        response_coro = self.stub.SandboxPayIn(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, sandbox_pb2.SandboxPayInRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "SandboxPayIn")
        return _grpc_helpers.protobuf_to_dataclass(response, SandboxPayInResponse)

    @handle_aio_request_error("GetSandboxWithdrawLimits")
    async def get_sandbox_withdraw_limits(
        self,
        *,
        account_id: str = "",
    ) -> WithdrawLimitsResponse:
        request = WithdrawLimitsRequest()
        request.account_id = account_id
        response_coro = self.stub.GetSandboxWithdrawLimits(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, operations_pb2.WithdrawLimitsRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(
            await get_tracking_id_from_coro(response_coro), "GetSandboxWithdrawLimits"
        )
        return _grpc_helpers.protobuf_to_dataclass(response, WithdrawLimitsResponse)


class StopOrdersService(_grpc_helpers.Service):
    _stub_factory = stoporders_pb2_grpc.StopOrdersServiceStub

    @handle_aio_request_error("PostStopOrder")
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
        response_coro = self.stub.PostStopOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.PostStopOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "PostStopOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, PostStopOrderResponse)

    @handle_aio_request_error("GetStopOrders")
    async def get_stop_orders(self, *, account_id: str = "") -> GetStopOrdersResponse:
        request = GetStopOrdersRequest()
        request.account_id = account_id
        response_coro = self.stub.GetStopOrders(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.GetStopOrdersRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "GetStopOrders")
        return _grpc_helpers.protobuf_to_dataclass(response, GetStopOrdersResponse)

    @handle_aio_request_error("CancelStopOrder")
    async def cancel_stop_order(
        self, *, account_id: str = "", stop_order_id: str = ""
    ) -> CancelStopOrderResponse:
        request = CancelStopOrderRequest()
        request.account_id = account_id
        request.stop_order_id = stop_order_id
        response_coro = self.stub.CancelStopOrder(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, stoporders_pb2.CancelStopOrderRequest()
            ),
            metadata=self.metadata,
        )
        response = await response_coro
        log_request(await get_tracking_id_from_coro(response_coro), "CancelStopOrder")
        return _grpc_helpers.protobuf_to_dataclass(response, CancelStopOrderResponse)
