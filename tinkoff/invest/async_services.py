# pylint:disable=redefined-builtin,too-many-lines
import asyncio
from datetime import datetime
from typing import AsyncGenerator, Optional

import grpc

from .grpc import (
    instruments_pb2_grpc,
    marketdata_pb2_grpc,
    operations_pb2_grpc,
    orders_pb2_grpc,
    sandbox_pb2_grpc,
    stoporders_pb2_grpc,
    users_pb2_grpc,
)
from .market_data_stream.async_market_data_stream_manager import (
    AsyncMarketDataStreamManager,
)
from .schemas import CandleInterval, HistoricCandle
from .typedefs import AccountId
from .utils import get_intervals, now


class AsyncServices:
    def __init__(
        self,
        channel: grpc.aio.Channel,
    ) -> None:
        self.instruments = instruments_pb2_grpc.InstrumentsServiceStub(channel)
        self.market_data = marketdata_pb2_grpc.MarketDataServiceStub(channel)
        self.market_data_stream = marketdata_pb2_grpc.MarketDataStreamServiceStub(
            channel
        )
        self.operations = operations_pb2_grpc.OperationsServiceStub(channel)
        self.operations_stream = operations_pb2_grpc.OperationsStreamServiceStub(
            channel
        )
        self.orders_stream = orders_pb2_grpc.OrdersStreamServiceStub(channel)
        self.orders = orders_pb2_grpc.OrdersServiceStub(channel)
        self.users = users_pb2_grpc.UsersServiceStub(channel)
        self.sandbox = sandbox_pb2_grpc.SandboxServiceStub(channel)
        self.stop_orders = stoporders_pb2_grpc.StopOrdersServiceStub(channel)

    def create_market_data_stream(self) -> AsyncMarketDataStreamManager:
        return AsyncMarketDataStreamManager(market_data_stream=self.market_data_stream)

    async def cancel_all_orders(self, account_id: AccountId) -> None:
        orders_service: orders_pb2_grpc.OrdersServiceStub = self.orders
        stop_orders_service: stoporders_pb2_grpc.StopOrdersServiceStub = (
            self.stop_orders
        )

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
        instrument_id: str = "",
    ) -> AsyncGenerator[HistoricCandle, None]:
        to = to or now()

        for local_from_, local_to in get_intervals(interval, from_, to):
            candles_response = await self.market_data.get_candles(
                figi=figi,
                interval=interval,
                from_=local_from_,
                to=local_to,
                instrument_id=instrument_id,
            )
            for candle in candles_response.candles:
                yield candle
