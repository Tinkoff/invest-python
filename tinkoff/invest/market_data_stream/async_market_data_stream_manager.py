import asyncio
import threading
from asyncio import Queue
from typing import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
)

from tinkoff.invest.schemas import MarketDataResponse, MarketDataRequest
from tinkoff.invest.market_data_stream.market_data_stream_interface import \
    IMarketDataStreamManager
from tinkoff.invest.market_data_stream.stream_managers import LastPriceStreamManager, \
    InfoStreamManager, TradesStreamManager, OrderBookStreamManager, CandlesStreamManager


class AsyncMarketDataStreamManager(IMarketDataStreamManager):
    def __init__(self, market_data_stream: "MarketDataStreamService"):
        self._market_data_stream_service = market_data_stream
        self._market_data_stream: AsyncIterator[MarketDataResponse]
        self._requests: Queue[MarketDataRequest] = Queue()
        self._unsubscribe_event = threading.Event()

    async def _get_request_generator(self) -> AsyncIterable[MarketDataRequest]:
        while not self._unsubscribe_event.is_set() or not self._requests.empty():
            if request := await self._requests.get():
                yield request

    @property
    def candles(self) -> "CandlesStreamManager[AsyncMarketDataStreamManager]":
        return CandlesStreamManager[AsyncMarketDataStreamManager](parent_manager=self)

    @property
    def order_book(self) -> "OrderBookStreamManager[AsyncMarketDataStreamManager]":
        return OrderBookStreamManager[AsyncMarketDataStreamManager](parent_manager=self)

    @property
    def trades(self) -> "TradesStreamManager[AsyncMarketDataStreamManager]":
        return TradesStreamManager[AsyncMarketDataStreamManager](parent_manager=self)

    @property
    def info(self) -> "InfoStreamManager[AsyncMarketDataStreamManager]":
        return InfoStreamManager[AsyncMarketDataStreamManager](parent_manager=self)

    @property
    def last_price(self) -> "LastPriceStreamManager[AsyncMarketDataStreamManager]":
        return LastPriceStreamManager[AsyncMarketDataStreamManager](parent_manager=self)

    def subscribe(self, market_data_request: MarketDataRequest) -> None:
        asyncio.run(self._requests.put(market_data_request))

    def unsubscribe(self, market_data_request: MarketDataRequest) -> None:
        asyncio.run(self._requests.put(market_data_request))

    def stop(self) -> None:
        self._unsubscribe_event.set()

    def __aiter__(self) -> "AsyncMarketDataStreamManager":
        self._unsubscribe_event.clear()
        self._market_data_stream = self._market_data_stream_service.market_data_stream(
            self._get_request_generator()
        ).__aiter__()

        return self

    def __anext__(self) -> Awaitable[MarketDataResponse]:
        return self._market_data_stream.__anext__()
